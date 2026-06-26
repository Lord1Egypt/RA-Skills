# 03 — Pre-Warm (Outbound Calls)

## The dead air problem

Standard cold-connect opens the OpenAI WebSocket inside the Twilio
/media-stream handler — AFTER the person answers. This creates 2-3 seconds
of silence at pickup, which most people interpret as a robocall.

## The fix: pre-warm

Open the OpenAI session BEFORE the phone rings. Buffer the greeting audio.
Flush the buffer the instant Twilio connects.

```
POST /outbound-call arrives
  → Open OpenAI WS immediately
  → session.update + response.create (greeting)
  → Buffer response.output_audio.delta chunks
  → Place Twilio call (phone starts ringing)
  → Person answers → Twilio /media-stream WS opens
  → Flush buffered greeting to Twilio instantly
  → AI speaking within ~100ms of pickup
```

## Session state map

```javascript
const preWarmSessions = new Map(); // callId → session

// Session shape:
{
  openaiWs: WebSocket,
  greetingBuffer: [],       // Array of base64 PCMU chunks
  greetingComplete: false,  // true when response.output_audio.done fires
  streamSid: null,          // Set when Twilio answers
  twilioWs: null,           // Set when Twilio answers
  callSid: null,            // Twilio CallSid (set at call creation)
  status: "warming",        // warming | ready | live | failed | expired
  createdAt: Date.now(),
}
```

## POST /outbound-call handler

```javascript
app.post("/outbound-call", async (req, res) => {
  const { to, prospectContext } = req.body;
  const callId = crypto.randomUUID();

  const openaiWs = new WebSocket(
    "wss://api.openai.com/v1/realtime?model=gpt-realtime-1.5",
    { headers: { Authorization: `Bearer ${process.env.OPENAI_API_KEY}` } }
  );

  const session = {
    openaiWs, greetingBuffer: [], greetingComplete: false,
    streamSid: null, twilioWs: null, callSid: null,
    status: "warming", createdAt: Date.now(),
  };
  preWarmSessions.set(callId, session);

  openaiWs.on("open", () => {
    setTimeout(() => {
      openaiWs.send(JSON.stringify({
        type: "session.update",
        session: {
          type: "realtime", model: "gpt-realtime-1.5",
          output_modalities: ["audio"],
          instructions: buildSystemPrompt(prospectContext),
          prompt_cache_key: "llc-outbound-v1",
          audio: {
            input: { format: { type: "audio/pcmu" }, turn_detection: {
              type: "semantic_vad", eagerness: "high",
              create_response: true, interrupt_response: true,
            }},
            output: { format: { type: "audio/pcmu" }, voice: "cedar" },
          },
        },
      }));
    }, 100);
  });

  openaiWs.on("message", (rawData) => {
    const event = JSON.parse(rawData);

    if (event.type === "session.updated") {
      openaiWs.send(JSON.stringify({
        type: "conversation.item.create",
        item: { type: "message", role: "user",
          content: [{ type: "input_text", text: "Greet the caller now." }],
        },
      }));
      openaiWs.send(JSON.stringify({ type: "response.create" }));
    }

    if ((event.type === "response.output_audio.delta" || event.type === "response.audio.delta") && event.delta) {
      session.greetingBuffer.push(event.delta);
    }

    if (event.type === "response.output_audio.done" || event.type === "response.audio.done") {
      session.greetingComplete = true;
      session.status = "ready";
      if (session.streamSid && session.twilioWs) flushGreetingBuffer(session);
    }
  });

  // 10-second fallback
  setTimeout(() => {
    const s = preWarmSessions.get(callId);
    if (s && s.status === "warming") {
      s.status = "failed";
      console.warn(`Pre-warm timeout for ${callId} — cold connect fallback`);
    }
  }, 10_000);

  // Place the call
  const call = await twilioClient.calls.create({
    from: process.env.TWILIO_PHONE_NUMBER,
    to,
    twiml: `<Response><Connect><Stream url="wss://${DOMAIN}/media-stream?callId=${callId}" /></Connect></Response>`,
    statusCallback: `https://${DOMAIN}/call-status`,
    statusCallbackMethod: "POST",
    statusCallbackEvent: ["completed", "no-answer", "busy", "failed"],
  });
  session.callSid = call.sid;
  callSidToCallId.set(call.sid, callId);

  res.json({ callSid: call.sid, callId });
});
```

## /media-stream handler (outbound)

```javascript
app.ws("/media-stream", (twilioWs, req) => {
  const callId = req.query.callId;
  const session = preWarmSessions.get(callId);

  if (!session || session.status === "failed") {
    handleColdConnect(twilioWs, req); return;
  }

  session.twilioWs = twilioWs;

  twilioWs.on("message", (message) => {
    const data = JSON.parse(message);

    if (data.event === "start") {
      session.streamSid = data.start.streamSid;
      if (session.greetingComplete) flushGreetingBuffer(session);
      // If still buffering, response.output_audio.done handler flushes
    }

    if (data.event === "media" && session.status === "live") {
      if (session.openaiWs.readyState === WebSocket.OPEN) {
        session.openaiWs.send(JSON.stringify({
          type: "input_audio_buffer.append",
          audio: data.media.payload,
        }));
      }
    }
  });

  session.openaiWs.on("message", (rawData) => {
    if (session.status !== "live") return;
    const event = JSON.parse(rawData);
    if (
      (event.type === "response.output_audio.delta" || event.type === "response.audio.delta") &&
      event.delta && session.streamSid
    ) {
      session.twilioWs.send(JSON.stringify({
        event: "media", streamSid: session.streamSid,
        media: { payload: event.delta },
      }));
    }
  });

  twilioWs.on("close", () => {
    if (session.openaiWs.readyState === WebSocket.OPEN) session.openaiWs.close();
    preWarmSessions.delete(callId);
  });
});
```

## Buffer flush function

```javascript
function flushGreetingBuffer(session) {
  if (!session.streamSid || !session.twilioWs) return;
  session.status = "live";
  for (const chunk of session.greetingBuffer) {
    session.twilioWs.send(JSON.stringify({
      event: "media", streamSid: session.streamSid,
      media: { payload: chunk },
    }));
  }
  session.greetingBuffer = [];
}
```

## Orphaned session cleanup

```javascript
// Twilio status webhook
app.post("/call-status", (req, res) => {
  const callId = callSidToCallId.get(req.body.CallSid);
  if (callId) {
    const session = preWarmSessions.get(callId);
    if (session?.openaiWs.readyState === WebSocket.OPEN) session.openaiWs.close();
    preWarmSessions.delete(callId);
    callSidToCallId.delete(req.body.CallSid);
  }
  res.sendStatus(200);
});

// Belt-and-suspenders sweeper (sessions older than 90s)
setInterval(() => {
  const now = Date.now();
  for (const [callId, session] of preWarmSessions.entries()) {
    if (now - session.createdAt > 90_000) {
      if (session.openaiWs.readyState === WebSocket.OPEN) session.openaiWs.close();
      preWarmSessions.delete(callId);
    }
  }
}, 30_000);
```

## Edge cases

| Scenario | Handled by |
|---|---|
| Twilio answers before greeting buffer complete | `response.output_audio.done` handler checks streamSid and flushes |
| Greeting complete before Twilio answers | `start` event handler checks greetingComplete and flushes |
| Barge-in during buffered replay | VAD stays active — OpenAI fires speech_started, response.cancel naturally |
| No answer / busy / voicemail | statusCallback webhook cleans up session |
| OpenAI session spike (10-12s init) | 10s timeout flips status to "failed", cold connect fallback |
| Buffer overflow (large greeting) | Use setImmediate between chunks if needed — see 07-twilio-integration.md |
