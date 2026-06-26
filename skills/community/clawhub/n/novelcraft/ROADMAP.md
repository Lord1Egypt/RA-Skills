# NovelCraft Roadmap

Planned features for future versions.

---

## 📊 Dashboard (Planned)

### Vision
A web-based dashboard for monitoring and controlling NovelCraft projects.

### Planned Features

| Feature | Description | Priority |
|---------|-------------|----------|
| **Project Overview** | List all projects with status (Concept → Publication) | High |
| **Live Progress** | Progress bars for current chapters | High |
| **Chapter Detail View** | View drafts, reviews, scores | Medium |
| **Control Panel** | Start/Pause, switch mode (autonomous/step-by-step) | Medium |
| **Logs & History** | Execution history, errors, revisions | Medium |
| **Config Editor** | Edit module configs directly in browser | Low |
| **Export Trigger** | Manual PDF/EPUB export | Low |

### Technical Considerations
- OpenClaw web integration or standalone UI
- WebSocket for live updates
- Optional: Authentication for multi-user

### Status
🚧 **In Planning** — Not yet in development

---

## 🔊 Audio (Planned)

### Vision
Audiobook generation from completed chapters.

### Planned Features

| Feature | Description | Priority |
|---------|-------------|----------|
| **TTS Integration** | Text-to-Speech for chapters | High |
| **Character Voices** | Different voices for dialogue | Medium |
| **Chapter Export** | MP3/WAV per chapter | High |
| **Audiobook Compilation** | Combine all chapters into one file | Medium |
| **Mood Adjustment** | Emotional intonation (whisper, shout) | Low |
| **Background Music** | Optional: Ambient/Atmosphere | Low |

### Technical Considerations

**Provider Options:**
| Provider | Advantage | Disadvantage |
|----------|-----------|--------------|
| **ElevenLabs API** | High quality, many voices | Cost, external API |
| **OpenAI TTS** | Good, simple | Cost, external API |
| **Local TTS** (Piper, Coqui) | Free, offline | Quality varies |
| **System TTS** | No installation | Quality usually poor |

**Configuration in `module-audio.md`:**
```yaml
enabled: false  # Default: disabled
provider: elevenlabs  # or openai, local, system
voice_mapping:
  narrator: "nova"
  protagonist: "onyx"
  antagonist: "echo"
format: mp3
quality: high
```

### Dependencies
- Optional: `ffmpeg` for audio processing
- Configure API keys externally (env vars)

### Status
🚧 **In Planning** — Concept phase

---

## Version Planning

| Version | Planned | Features |
|---------|---------|----------|
| **3.1.0** | Q2 2026 | Dashboard v1 (Overview, Progress) |
| **3.2.0** | Q3 2026 | Dashboard v2 (Control, Config-Editor) |
| **4.0.0** | Q4 2026 | Audio v1 (TTS Integration, MP3 Export) |
| **4.1.0** | 2027 | Audio v2 (Character Voices, Audiobook) |

---

## Contributing

Have ideas for Dashboard or Audio?
- Create an issue on GitHub
- Or discuss in the OpenClaw Discord

---

*Last updated: 2026-04-06*
