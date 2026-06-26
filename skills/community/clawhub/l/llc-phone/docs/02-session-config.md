# 02 — Session Configuration Reference

## Connecting to the Realtime API (WebSocket)

```javascript
import WebSocket from "ws";

const openAiWs = new WebSocket(
  "wss://api.openai.com/v1/realtime?model=gpt-realtime-1.5",
  {
    headers: {
      Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
    },
  }
);
```

Wait for `open`, then wait for `session.created` from the server before
sending `session.update`. If your implementation has race conditions during
startup, a short delay can be a practical workaround, but prefer driving from
actual events rather than timing assumptions.

## Recommended session.update (Twilio/PCMU — outbound or inbound default)

```javascript
const sessionUpdate = {
  type: "session.update",
  session: {
    type: "realtime",
    model: "gpt-realtime-1.5",
    output_modalities: ["audio"],
    instructions: SYSTEM_PROMPT,            // Static prefix first for caching
    prompt_cache_key: "llc-outbound-v1",    // Stable — change when prompt changes
    tools: OPENING_TOOLS,                   // Lean toolset for first turn only
    audio: {
      input: {
        format: { type: "audio/pcmu" },
        turn_detection: {
          type: "semantic_vad",
          eagerness: "high",                // Fast first-turn response
          create_response: true,
          interrupt_response: true,
        },
      },
      output: {
        format: { type: "audio/pcmu" },
        voice: "cedar",
      },
    },
    // input_audio_noise_reduction: null    // Leave unset for outbound calls
  },
};
```

## Triggering the opening greeting

```javascript
openaiWs.on("message", (rawData) => {
  const event = JSON.parse(rawData);
  if (event.type === "session.updated") {
    // Session is configured — trigger greeting
    openaiWs.send(JSON.stringify({
      type: "conversation.item.create",
      item: {
        type: "message",
        role: "user",
        content: [{ type: "input_text", text: "Greet the caller now. Start speaking immediately." }],
      },
    }));
    openaiWs.send(JSON.stringify({ type: "response.create" }));
  }
});
```

## Audio event names

In current realtime integrations you may encounter `response.output_audio.delta`
and, in older examples or model families, `response.audio.delta`. If you need
broad compatibility, handle both:

```javascript
// Receiving audio FROM OpenAI (send to Twilio):
if (
  (event.type === "response.output_audio.delta" ||
   event.type === "response.audio.delta") &&
  event.delta
) {
  twilioWs.send(JSON.stringify({
    event: "media",
    streamSid: streamSid,
    media: { payload: event.delta }, // Already base64 PCMU
  }));
}

// Audio done (greeting complete):
if (
  event.type === "response.output_audio.done" ||
  event.type === "response.audio.done"
) {
  // Greeting buffer is complete (outbound pre-warm)
  // or first turn done (switch VAD eagerness, add full toolset)
}
```

## Sending caller audio TO OpenAI (from Twilio):

```javascript
if (data.event === "media" && openaiWs.readyState === WebSocket.OPEN) {
  openaiWs.send(JSON.stringify({
    type: "input_audio_buffer.append",
    audio: data.media.payload,
  }));
}
```

## Switching VAD and adding tools after first turn

```javascript
// After first AI turn completes (response.done event):
openaiWs.send(JSON.stringify({
  type: "session.update",
  session: {
    audio: {
      input: {
        turn_detection: {
          type: "semantic_vad",
          eagerness: "medium", // Less jumpy for natural conversation
          create_response: true,
          interrupt_response: true,
        },
      },
    },
    tools: FULL_TOOL_SET, // Add CRM, calendar, escalation tools now
  },
}));
```

## Voice options

| Voice | Character | Notes |
|---|---|---|
| `cedar` | Neutral, professional | Good starting point for B2B outbound |
| `marin` | Warm, conversational | Good starting point for receptionist / consumer calls |
| `alloy` | Neutral, clear | Legacy — widely tested |
| `ash` | Calm, measured | Good for support |
| `coral` | Bright, energetic | Good for sales |
| `echo` | Deep, authoritative | Legacy |
| `sage` | Balanced | General-purpose |
| `shimmer` | Clear, younger | Legacy |
| `verse` | Expressive | Validate carefully in production call flows |

Voice cannot be changed after the model has produced audio. Set it in the
first session.update.

## Prompt structure for maximum cache hits

```
[STATIC — identical every call for this campaign]
Role, instructions, rules, tone guidelines, tool descriptions

---
[DYNAMIC — appended per call]
Caller/prospect context: name, company, goal, history
```

Set `prompt_cache_key` to a stable string per campaign (for example,
`"llc-outbound-v1"`). Change it only when the static prefix changes. Prompt
caching can materially reduce repeated-prefix overhead on longer prompts.

## Model-page limits to keep in mind

- Current OpenAI model pages list a 32,000-token context window for
  `gpt-realtime-1.5`
- Current OpenAI model pages list 4,096 max output tokens for
  `gpt-realtime-1.5`
- Validate realtime session duration and long-call behavior against current
  docs and your own production tests
