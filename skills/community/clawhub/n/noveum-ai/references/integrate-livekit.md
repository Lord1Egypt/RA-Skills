# Integrate: LiveKit Agents (voice)

Voice integrations capture both conversation content AND voice telemetry (STT/TTS timing,
latency). The latency scorers only work if the wrappers are installed — a "working"
integration without them silently produces unmeasurable latency evals.

## 1. Install and initialize

```bash
pip install "noveum-trace[livekit]"
```

```python
import noveum_trace
noveum_trace.init(project="<NOVEUM_PROJECT>", environment="production")
```

## 2. Wrap STT/TTS and hook the session

```python
from noveum_trace.integrations.livekit import (
    LiveKitSTTWrapper,
    LiveKitTTSWrapper,
    setup_livekit_tracing,
)

traced_stt = LiveKitSTTWrapper(stt=deepgram.STT(model="nova-2"), session_id=ctx.job.id)
traced_tts = LiveKitTTSWrapper(tts=cartesia.TTS(model="sonic-english"), session_id=ctx.job.id)

session = AgentSession(stt=traced_stt, tts=traced_tts, llm=llm, vad=vad)
setup_livekit_tracing(session)   # auto-creates the trace on session.start()
```

There is also `LiveKitLLMWrapper` for per-call LLM detail if the session-level capture
isn't enough.

## 3. What must be present for voice evals

After integration, traces must carry: conversation turns (user + assistant), LLM metrics,
function/tool calls, and the timing telemetry the wrappers emit (STT delay, TTS TTFB,
end-to-end latency). `scripts/check_integration.py` checks these — run it with
`--voice` so voice telemetry is required, not optional.

## 4. Lifecycle

Agent workers are long-running; ensure `noveum_trace.shutdown()` runs on worker shutdown
(atexit or the framework's shutdown hook) so the final session's batch flushes.

Proceed to `verify-traces.md` for the acceptance check.
