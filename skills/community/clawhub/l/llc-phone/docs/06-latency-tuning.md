# 06 — Latency Tuning (After Pre-Warm / Pre-Accept)

Pre-warm (outbound) and pre-accept warm (inbound) handle the initialization
dead air. These levers trim per-turn latency during live conversation.

## The practical floor

The exact floor depends on region, model, prompt size, and transport path. In
practice, sub-second voice-to-voice interactions are possible in well-tuned
realtime phone stacks, but you should benchmark your own deployment.

Anything under 1 second usually feels natural. Between 1 and 2 seconds starts
to feel delayed. Beyond 2 seconds tends to feel robotic.

## Lever 1: Semantic VAD with eagerness: "high" (first turn)

`semantic_vad` can be a useful first-turn starting point when you want fast,
natural turn-taking, but it should be validated against `server_vad` in your
own environment.

```json
"turn_detection": {
  "type": "semantic_vad",
  "eagerness": "high",
  "create_response": true,
  "interrupt_response": true
}
```

Switch to `"medium"` after the first AI turn if you want less aggressive
mid-conversation turn-taking:

```javascript
// After response.done for turn 1:
openaiWs.send(JSON.stringify({
  type: "session.update",
  session: { audio: { input: { turn_detection: {
    type: "semantic_vad", eagerness: "medium",
    create_response: true, interrupt_response: true,
  }}}},
}));
```

## Lever 2: Prompt caching

Prompt caching can materially reduce repeated-prefix overhead on longer prompts.

Rules:
1. Set `prompt_cache_key` to a stable string per campaign or mode.
2. Keep static instructions at the top of your prompt.
3. Put dynamic caller or prospect data at the bottom after a separator.
4. Do not put dates, call IDs, or other call-specific content at the top.

Expected hit behavior depends on prompt stability and traffic shape.

## Lever 3: Lean opening turn toolset

Every tool description in the session adds inference overhead. For the first
turn, load only the minimum tools needed. Add the full toolset via a second
`session.update` after turn 1:

```javascript
openaiWs.send(JSON.stringify({
  type: "session.update",
  session: { tools: FULL_TOOL_SET },
}));
```

## Lever 4: Test with noise reduction unset

If you observe latency regressions or unstable turn-taking, test with
`input_audio_noise_reduction` unset and compare results in your environment.

## Lever 5: Twilio edge colocation

Place your server close to the expected Twilio edge and caller population where
practical, and verify any SDK- or account-level edge configuration against
current Twilio docs.

## Lever 6: Model selection

Use `gpt-realtime-1.5` as the highest-capability default in this package. Test
`gpt-realtime-mini` when lower cost matters more than top-end capability.

## Latency budget

| Component | Controllable | Notes |
|---|---|---|
| Pre-warm / pre-accept init | YES | Handled before call connects |
| Turn detection delay | YES | Validate `semantic_vad` and `server_vad` |
| Prompt cache overhead | YES | Depends on prompt reuse |
| Model inference | NO | Model- and workload-dependent |
| Twilio transport | Partially | Improve by keeping network path short |
| Buffer flush | YES | Important for pre-warm / pre-accept patterns |

## What not to do

- Do not add artificial hold music or "thinking" beeps if your goal is a
  natural human-like interaction.
- Do not wait for AMD result before connecting the stream if your goal is to
  preserve the pre-warm benefit.
- Do not set `silence_duration_ms` very low with `server_vad` without testing
  false-positive turn cuts.
