# ACE-Step Local Music Generation

Open source music generation model for local deployment.

## Overview

ACE-Step is an optional local AI component. Users choose whether to install it.

## Installation (User-Initiated)

```bash
# User manually clones and installs
git clone https://github.com/ace-step/ace-step.git
cd ace-step
pip install -r requirements.txt
```

## Model Weights (Downloaded by User)

If users choose to use ACE-Step, they download model weights themselves:

```python
# First run downloads weights to local cache (~4GB)
from ace_step import MusicGenerator
generator = MusicGenerator.from_pretrained("ace-step/base")
```

- Download happens once, cached locally
- No automatic downloads without user action
- Weights stay on user's machine

## Usage in This Skill

```python
# Only if user has installed ACE-Step
from ace_step import MusicGenerator

audio = generator.generate_from_midi(
    midi_path="input.mid",
    style="pop",
    duration=120
)
audio.save("output.mp3")
```

## Alternative (No AI Required)

Default mode uses SoundFont synthesis - no AI models, no downloads:

```python
import pretty_midi
pm = pretty_midi.PrettyMIDI("input.mid")
audio = pm.fluidsynth(fs=44100)  # Local synthesis
```

## Privacy

- All generation happens locally
- No data sent to external servers
- User controls all downloads
