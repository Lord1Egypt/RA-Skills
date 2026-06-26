# Music & Audio

## Music Playback
- **spotify-player** — Spotify search/playback via spogo
- **sonoscli** — Sonos speaker control (discover, play, volume, group)
- **blucli** — BluOS multi-room audio

## Music Generation
- ClawHub: ACE Music (free Suno alternative), ElevenLabs music
- AI music via API services
- Generate with lyrics, genre, mood specifications

## Text-to-Speech
- **sag** — ElevenLabs TTS (high quality, multiple voices)
- **sherpa-onnx-tts** — Offline TTS (no cloud needed)
- OpenAI TTS API

## Speech-to-Text
- **openai-whisper** — Local Whisper (no API key)
- **openai-whisper-api** — Cloud Whisper API
- For transcripts, use `summarize` skill

## Audio Analysis
- **songsee** — Spectrograms, feature panels
- **ffmpeg** — Audio metadata, format conversion
- librosa (Python) for advanced analysis

## Audio Processing
```bash
# Convert format
ffmpeg -i input.wav output.mp3

# Trim audio
ffmpeg -i input.mp3 -ss 00:00:30 -to 00:01:30 output.mp3

# Adjust volume
ffmpeg -i input.mp3 -filter:a "volume=1.5" output.mp3

# Merge audio files
ffmpeg -i "concat:1.mp3|2.mp3|3.mp3" -c copy merged.mp3

# Extract audio from video
ffmpeg -i video.mp4 -vn -q:a 2 audio.mp3
```

## Podcast Workflow
1. Record/transcribe audio (whisper)
2. Generate show notes (summarize)
3. Edit with ffmpeg
4. Publish to hosting platform

## Sound Effects & Samples
- Freesound.org API
- Generate with audio synthesis tools
- Layer and mix with ffmpeg/sox
