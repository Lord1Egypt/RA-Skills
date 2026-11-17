# Integrate: Pipecat (voice)

Pipecat integration is observer-based: a frame observer traces turns, STT/TTS/LLM spans,
and can capture full stereo audio for audio scorers.

## 1. Install and initialize

```bash
pip install "noveum-trace[pipecat]"
```

```python
import noveum_trace
noveum_trace.init(project="<NOVEUM_PROJECT>", environment="production")
```

## 2. Attach the observer to the pipeline task

```python
from noveum_trace.integrations.pipecat import setup_pipecat_tracing

observer = setup_pipecat_tracing(record_audio=True)  # audio capture feeds audio scorers

task = PipelineTask(pipeline, observers=[observer])
await observer.attach_to_task(task)
```

`record_audio=True` uses an `AudioBufferProcessor` to capture stereo WAV per conversation —
required for MOS/pronunciation/audio-quality scorers; skip it only if the user declines
audio storage.

Transport note: noveum-trace ships transport subclasses for Daily / LiveKit / WebRTC /
Websocket / Tavus / HeyGen — use the matching one if the app uses a custom transport and
frames aren't being observed.

## 3. What must be present for voice evals

A healthy Pipecat integration emits (per production deployments): `turn.number` /
`turn.duration_seconds` / `turn.user_input` / `turn.user_bot_latency_seconds`,
`stt.text` / `stt.first_text_latency_ms` / `stt.vad_to_final_ms`,
`tts.time_to_first_byte_ms` / `tts.input_text`, `llm.model` / `llm.input` / token+cost
attrs / `llm.time_to_first_token_ms` / `llm.function_calls`, and
`full_conversation.audio_*` when audio capture is on. Verify with
`scripts/check_integration.py --voice`.

## 4. Lifecycle

Ensure `noveum_trace.shutdown()` on worker/process shutdown (atexit or framework hook).

Proceed to `verify-traces.md` for the acceptance check.
