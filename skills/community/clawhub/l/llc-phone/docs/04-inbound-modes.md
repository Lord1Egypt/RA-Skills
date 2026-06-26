# 04 — Inbound Call Modes

## Pre-Accept Warm (inbound equivalent of pre-warm)

When Twilio receives an inbound call, it POSTs to your webhook BEFORE
bridging audio. The call is ringing but no audio is flowing yet. This is
your pre-accept window — open the OpenAI session now.

```
Inbound call => Twilio POSTs to /inbound-webhook
  => Server opens OpenAI WS immediately
  => session.update + response.create (greeting)
  => Buffer greeting audio chunks
  => Respond with TwiML: <Connect><Stream>
  => Twilio bridges audio => stream connects
  => Flush buffered greeting => caller hears AI within ~100ms
```

## /inbound-webhook handler

```javascript
app.post("/inbound-webhook", async (req, res) => {
  const { CallSid, From, To } = req.body;
  const callId = CallSid;
  const modeConfig = getModeConfig(To, From);
  const openaiWs = new WebSocket(
    "wss://api.openai.com/v1/realtime?model=gpt-realtime-1.5",
    { headers: { Authorization: `Bearer ${process.env.OPENAI_API_KEY}` } }
  );
  const session = {
    openaiWs, greetingBuffer: [], greetingComplete: false,
    streamSid: null, twilioWs: null, callSid: CallSid,
    status: "warming", mode: modeConfig.mode,
    callerNumber: From, createdAt: Date.now(),
  };
  preWarmSessions.set(callId, session);

  openaiWs.on("open", () => {
    setTimeout(() => {
      openaiWs.send(JSON.stringify({
        type: "session.update",
        session: {
          type: "realtime", model: "gpt-realtime-1.5",
          output_modalities: ["audio"],
          instructions: modeConfig.systemPrompt,
          prompt_cache_key: modeConfig.cacheKey,
          tools: modeConfig.tools,
          audio: {
            input: { format: { type: "audio/pcmu" }, turn_detection: {
              type: "semantic_vad", eagerness: "high",
              create_response: true, interrupt_response: true,
            }},
            output: { format: { type: "audio/pcmu" }, voice: modeConfig.voice },
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
          content: [{ type: "input_text", text: modeConfig.greetingPrompt }],
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

  setTimeout(() => {
    const s = preWarmSessions.get(callId);
    if (s && s.status === "warming") s.status = "failed";
  }, 10_000);

  res.type("text/xml").send(
    '<Response><Connect><Stream url="wss://' + DOMAIN + '/media-stream?callId=' + CallSid + '" /></Connect></Response>'
  );
});
```

## Mode routing

```javascript
function getModeConfig(toDid, fromNumber) {
  if (toDid === process.env.IVR_DID)          return ivrConfig(fromNumber);
  if (toDid === process.env.RECEPTIONIST_DID) return receptionistConfig(fromNumber);
  if (toDid === process.env.CSR_DID)          return csrConfig(fromNumber);
  return receptionistConfig(fromNumber); // default
}
```

---

## Mode 1: AI IVR (Route, Transfer, Warm Conference Transfer)

Natural language routing. Caller says what they need; AI routes them.
Supports cold transfer and warm conference-bridge hand-off.

### System prompt

```
You are an inbound call router for [Company].
Understand what the caller needs and route them. Do NOT solve their problem.
Available: Sales, Support, Billing, Scheduling.
Once you know where they need to go, use the transfer_call tool.
Greeting: "Thanks for calling [Company], how can I direct your call?"
```

### IVR tools (see 05-async-tools.md for implementation)

- `transfer_call(destination, reason)` — cold transfer to department or voicemail
- `warm_transfer(agent_number, introduction)` — conference in human, make intro, drop off
- `hang_up()` — end the call

### Cold transfer

```javascript
async function handleTransferCall(callSid, destination) {
  const map = {
    sales: process.env.SALES_NUMBER,
    support: process.env.SUPPORT_NUMBER,
    billing: process.env.BILLING_NUMBER,
    scheduling: process.env.SCHEDULING_NUMBER,
  };
  if (destination === "voicemail") {
    await twilioClient.calls(callSid).update({
      twiml: "<Response><Say>Please leave a message after the tone.</Say><Record /></Response>",
    });
    return;
  }
  await twilioClient.calls(callSid).update({
    twiml: "<Response><Dial>" + map[destination] + "</Dial></Response>",
  });
}
```

### Warm conference transfer

```javascript
async function handleWarmTransfer(callSid, agentNumber, introduction) {
  const confName = "xfer-" + callSid;
  // Move caller into conference
  await twilioClient.calls(callSid).update({
    twiml: "<Response><Say>One moment.</Say><Dial><Conference>" + confName + "</Conference></Dial></Response>",
  });
  // Dial agent into same conference
  await twilioClient.calls.create({
    from: process.env.TWILIO_PHONE_NUMBER, to: agentNumber,
    twiml: "<Response><Say>Transfer: " + introduction + "</Say><Dial><Conference>" + confName + "</Conference></Dial></Response>",
  });
}
```

---

## Mode 2: Receptionist

Greets by company name, identifies caller needs, checks availability,
routes or takes a structured message.

### System prompt

```
You are the receptionist for [Company Name].
Greet: "Good [morning/afternoon], [Company], this is [Voice Name] speaking."
Goals: 1) identify who is calling and what they need, 2) check if the right
person is available (use check_availability), 3) transfer if available,
4) take a message with name, number, and reason if not.
Keep responses natural and concise. Never leave silence > 20s without
checking back in.
```

### Receptionist tools

- `check_availability(person_or_dept)` — is staff member/dept available?
- `take_message(caller_name, caller_number, message, urgency)` — save message
- `transfer_call(destination_number, warm)` — route to person or dept
- `hang_up()` — end call politely

### Config factory

```javascript
function receptionistConfig(fromNumber) {
  return {
    mode: "receptionist",
    cacheKey: "llc-receptionist-v1",
    voice: "marin",
    tools: receptionistTools,
    systemPrompt: "You are the receptionist for [Company]...",
    greetingPrompt: "Greet the caller warmly as the receptionist.",
  };
}
```

---

## Mode 3: CSR with DB (Customer Service + Database)

Full customer service agent: look up account by caller phone, retrieve
history, book/reschedule appointments, add call notes, escalate.

### System prompt

```
You are a customer service representative for [Company].
When a call connects, silently look up the caller by phone using lookup_customer.
If found, greet by name. If not found, greet generically and ask for their name.
You can: answer account questions, update records, book or reschedule
appointments, add call notes, and escalate to a human if needed.
Always confirm changes back to the customer before saving.
Use natural filler while tools run: "Let me pull that up...", "One moment..."
```

### CSR tools

- `lookup_customer(phone)` — find record by E.164 phone number
- `get_appointments(customer_id, limit)` — retrieve upcoming appointments
- `book_appointment(customer_id, datetime_iso, service_type, notes)` — book
- `add_call_note(customer_id, note, outcome)` — save note to CRM
- `escalate_to_human(reason, customer_id, summary)` — transfer with context
- `hang_up()` — end call

### Silent background lookup on connect

```javascript
// greetingPrompt for CSR mode:
const greetingPrompt =
  "[SYSTEM] Caller phone: " + fromNumber + ". " +
  "Run lookup_customer silently using this number, then greet them. Start speaking immediately.";
```

In many realtime voice flows, the model can start greeting while
`lookup_customer` runs in the background. Treat that as a behavior to validate
in your own stack rather than as a guaranteed outcome.

---

## Mode config factory (complete)

```javascript
function ivrConfig(from) {
  return { mode: "ivr", cacheKey: "llc-ivr-v1", voice: "cedar",
    tools: ivrTools, systemPrompt: IVR_PROMPT,
    greetingPrompt: "Greet briefly and ask how to direct their call." };
}
function receptionistConfig(from) {
  return { mode: "receptionist", cacheKey: "llc-receptionist-v1", voice: "marin",
    tools: receptionistTools, systemPrompt: RECEPTIONIST_PROMPT,
    greetingPrompt: "Greet warmly as the receptionist." };
}
function csrConfig(from) {
  return { mode: "csr", cacheKey: "llc-csr-v1", voice: "cedar",
    tools: csrTools, systemPrompt: CSR_PROMPT,
    greetingPrompt: "[SYSTEM] Caller: " + from + ". Look them up silently and greet." };
}
```

## Inbound prompt cache keys

Use separate, stable cache keys per mode so each mode builds its own cache:
- IVR: `"llc-ivr-v1"`
- Receptionist: `"llc-receptionist-v1"`
- CSR: `"llc-csr-v1"`
