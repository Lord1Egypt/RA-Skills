# Basic Pitch Reference

Basic Pitch is Spotify's open-source audio-to-MIDI model. In Hum2Song it is the main tool for extracting note events from humming or singing recordings.

## What It Is Used For

- convert monophonic or light polyphonic melody recordings into MIDI
- recover note timing, pitch, and velocity estimates
- produce a MIDI object that can be cleaned before arrangement or synthesis

## Install

```bash
pip install basic-pitch
```

## Minimal Example

```python
from basic_pitch import ICASSP_2022_MODEL_PATH
from basic_pitch.inference import predict

model_output, midi_data, note_events = predict("audio_file.wav")
midi_data.write("output.mid")
```

## Output Notes

- `model_output`: raw model predictions
- `midi_data`: PrettyMIDI object for downstream processing
- `note_events`: note-level event list for inspection or debugging

## References

- GitHub: https://github.com/spotify/basic-pitch
- Paper: https://arxiv.org/abs/2203.09893
