# Librosa Reference

Librosa is a Python library for music and audio analysis. In Hum2Song it is useful for loading source audio, inspecting tempo, and extracting lightweight analysis features before MIDI or synthesis steps.

## Common Uses In This Skill

- load input audio and normalize sample rate
- estimate beat or tempo information
- inspect pitch-related information
- derive spectral features for debugging or preprocessing

## Install

```bash
pip install librosa
```

## Minimal Examples

### Load Audio

```python
import librosa

y, sr = librosa.load("audio.wav", sr=44100)
```

### Beat Tracking

```python
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)
```

### Pitch Tracking

```python
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
```

### Spectral Features

```python
D = librosa.stft(y)
mel_spec = librosa.feature.melspectrogram(y=y, sr=sr)
chroma = librosa.feature.chroma_stft(y=y, sr=sr)
```

## References

- Website: https://librosa.org/
- Docs: https://librosa.org/doc/latest/
- GitHub: https://github.com/librosa/librosa
