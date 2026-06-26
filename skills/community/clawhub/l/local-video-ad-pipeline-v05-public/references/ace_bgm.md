# ACE-Step BGM

Local Gradio UI: `F:\AI\ACE-Step\start_gradio_ui_rocm.bat`.

Set `CHECK_UPDATE=false` for unattended runs. Otherwise the launcher can hang on an update-check prompt.

## Capabilities

- 30-180 second music generation.
- Instrumental or lyric-based tracks.
- Lightning preset can produce a short commercial cue quickly on Strix Halo.
- Prompt in English for best style control.

## API

`fire_bgm.py` connects to the Gradio app and auto-discovers the generation endpoint by inspecting labels such as `Music Caption` and `Audio Duration (seconds)`.

If ACE-Step changes its UI and discovery fails, inspect dependencies:

```python
from gradio_client import Client
c = Client("http://127.0.0.1:7860")
for i, dep in enumerate(c.config["dependencies"]):
    print(i, dep.get("api_name"), dep.get("inputs"))
```

Then pass the endpoint manually:

```bash
python scripts/fire_bgm.py --fn-index 121 --out <project>/audio/bgm.wav
```

## Prompt Patterns

- Dark cinematic trap: `dark cinematic trap, hard-hitting 808 bass, gritty distorted synths, tense crescendo, percussive hi-hats, 130 bpm, instrumental, no vocals`
- Uplift commercial: `warm acoustic guitar, claps, soft strings swell, optimistic build, 110 bpm, instrumental, no vocals`
- Horror sting: `atonal strings, pulsing bass drone, distant chimes, 60 bpm, instrumental, no vocals`

Always specify `instrumental, no vocals` unless lyrics are wanted.

## GPU Coexistence

ACE-Step and Wan2.2 should not share the GPU on the 96 GB UMA host.

1. Finish Wan2.2 jobs.
2. Run `wsl --shutdown`.
3. Start ACE-Step.
4. Run `fire_bgm.py`.
