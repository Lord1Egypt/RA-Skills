# 08 — Operational Notes, Field Reports & Watch-Later Items

These notes are intentionally split from vendor-authoritative documentation.
They reflect practitioner reports and implementation lessons gathered on
2026-04-02 and should be validated in your own environment.

## Field reports to validate

### 1. Progressive latency creep in long sessions

Symptom: some practitioners report that early turns are responsive and later
turns become noticeably slower as the session grows.

Workaround: for calls expected to run long, test a session-refresh strategy
that carries forward a condensed conversation summary.

Status: treat as a long-call test case, not as a guaranteed vendor-known bug.

---

### 2. Voice naturalness trade-offs across model families

Symptom: perceived voice naturalness can vary materially across realtime model
families and voices.

Workaround: test your actual prompts and call flows on the voices and models
you plan to ship.

---

### 3. Accent and dialect consistency

Symptom: accent-control prompts may not produce the exact result you want.

Workaround: test accent requirements explicitly before making them part of the
product promise.

---

### 4. Performed emotion and expressive delivery

Symptom: some teams report that highly expressive or performative styles are
less reliable than straightforward conversational delivery.

Workaround: avoid product designs that depend on highly specific performed
emotion unless you have validated them in production-like testing.

---

### 5. Noise reduction plus turn detection interactions

Symptom: some stacks show turn-taking regressions when noise reduction and
aggressive turn detection are combined.

Workaround: compare behavior with `input_audio_noise_reduction` unset.

Status: treat as a troubleshooting hypothesis to test in your stack.

---

### 6. Occasional slow initialization spikes

Symptom: some sessions initialize much slower than the norm.

Workaround: keep the pre-warm / pre-accept timeout and cold-connect fallback in
place, and monitor initialization durations.

---

### 7. `server_vad` can complicate tool-heavy flows

Symptom: some tool-heavy flows behave differently under `server_vad` than under
`semantic_vad`.

Workaround: test both and use whichever gives the best balance of latency and
turn reliability.

---

### 8. Voice changes after first audio

Symptom: changing voice after the model has already emitted audio may not work
the way you expect.

Workaround: set your intended voice in the first `session.update`.

---

### 9. Be careful sending `response.create` after tool results

Symptom: if the model is already continuing naturally, another
`response.create` can create duplicate or garbled audio.

Workaround: only send `response.create` after tool results when your tested
flow actually requires it.

---

## Watch-later items

### A. `gpt-realtime-mini` evaluation

OpenAI currently lists `gpt-realtime-mini` as an available lower-cost realtime
model. Re-benchmark before swapping it into production call flows.

### B. Native SIP production readiness

If you are considering OpenAI SIP or a non-Twilio media path, evaluate it as a
separate architecture and benchmark it directly.

### C. Realtime model updates

Re-check OpenAI's changelog and model pages before every publish or major
rollout.

### D. MCP and tool orchestration maturity

If you depend on MCP or richer tool orchestration in realtime sessions, test
those flows directly rather than assuming parity with text-first workflows.

### E. Numeric eagerness values

Use the documented string values such as `"low"`, `"medium"`, `"high"`, and
`"auto"` rather than relying on community examples that use numeric settings.

---

## Changelog monitoring

- https://platform.openai.com/docs/changelog
- https://community.openai.com
- https://openai.com/index/
