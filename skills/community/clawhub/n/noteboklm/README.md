# OpenClaw NotebookLM Skill

Full Google NotebookLM integration for OpenClaw — programmatic access to all Studio features.

> OpenClaw handles installation and setup automatically.

**Source library:** [teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py)
**⚠️ Unofficial** — Uses undocumented Google APIs. May break without notice.

---

## What Can It Do?

| Feature | Description |
|---------|-------------|
| 📂 Add Sources | URLs, PDFs, YouTube, Google Drive, audio/video/images |
| 💬 Chat & Q&A | Ask questions with cited source references |
| 🎙️ Podcast | Generate and download Audio Overviews |
| 🎬 Video | Explainer and cinematic video generation |
| 📊 Slide Deck | PDF or editable PPTX download |
| ❓ Quiz | Multiple difficulty levels; JSON/Markdown/HTML export |
| 🃏 Flashcards | Study cards in multiple formats |
| 🗺️ Mind Map | Instant hierarchical JSON |
| 📈 Infographic | Multiple styles and orientations |
| 📋 Data Table | CSV export |
| 📄 Report | Briefing doc, study guide, blog post, custom |
| 📝 Notes | Save answers and history as notebook notes |
| 🌐 Web Research | Auto-discover and import sources |
| 📤 Export | Google Docs / Sheets |
| 🔒 Sharing | Programmatic permission management |

## Features Not Available in the Web UI

- ✅ Batch artifact downloads (`--all`)
- ✅ Quiz / Flashcard export as JSON, Markdown, or HTML
- ✅ Mind map JSON export for visualization tools
- ✅ Slide deck as PPTX (web UI: PDF only)
- ✅ Individual slide revision with natural language
- ✅ Report template customization (`--append`)
- ✅ Source full-text access
- ✅ Save Q&A and chat history as notebook notes
- ✅ Programmatic sharing and permission management

---

## First-Time Setup

OpenClaw installs the library. You only need to authenticate once:

```bash
notebooklm login    # Opens browser — log in with Google account
notebooklm list     # Confirm it works
```

Full documentation: [SKILL.md](SKILL.md)
Upstream docs: https://github.com/teng-lin/notebooklm-py
