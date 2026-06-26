---
name: notebooklm-integration
description: "Integrate Google NotebookLM capabilities into your workflow via the unofficial notebooklm-py library. Use when you need to: create/manage notebooks, import sources (URLs, PDFs, YouTube, etc.), run research queries, generate audio/video overviews, create slide decks/infographics/quizzes/flashcards, or download generated artifacts. Provides programmatic access to NotebookLM features not exposed in the web UI."
---
# NotebookLM Integration Skill

This skill enables you to leverage the full power of Google NotebookLM through the unofficial `notebooklm-py` Python library. It provides programmatic access to features that aren't available in the web UI, including batch operations, custom format exports, and advanced automation capabilities.

## When to Use This Skill

Use this skill when you need to:
- Create, list, rename, or delete NotebookLM notebooks
- Import various source types (URLs, YouTube videos, PDFs, text files, Google Drive, etc.)
- Ask questions and chat with your notebooks using custom personas
- Run web and Drive research agents with auto-import capabilities
- Generate Audio Overviews (podcasts) in multiple formats and languages
- Create Video Overviews with different visual styles
- Generate Slide Decks (PDF/PPTX) and Infographics (PNG)
- Create Quizzes and Flashcards in multiple formats (JSON, Markdown, HTML)
- Download all generated artifacts locally or export to Google Docs/Sheets
- Share notebooks with specific permissions and view level controls

## Quick Start

### Installation
First, ensure you have the notebooklm-py library installed:
```bash
pip install notebooklm-py
```

### Basic Usage Patterns

#### Python API
```python
from notebooklm import NotebookLMClient

# Initialize client
client = NotebookLMClient()

# Create a new notebook
notebook = client.create_notebook("My Research Project")

# Add sources
notebook.add_source(url="https://example.com/research-paper.pdf")
notebook.add_source(youtube_url="https://youtube.com/watch?v=abc123")
notebook.add_source(file_path="./documents/report.txt")

# Ask questions
response = notebook.ask("What are the main findings in these sources?")
print(response.text)

# Generate audio overview
audio = notebook.generate_audio_overview(
    format="deep-dive",
    length="medium",
    language="en"
)
audio.save("./outputs/podcast.mp3")
```

#### CLI Usage
```bash
# Create notebook
notebooklm notebook create "My Research"

# Add sources
notebooklm notebook add-source "My Research" --url https://example.com/paper.pdf
notebooklm notebook add-source "My Research" --youtube https://youtube.com/watch?v=abc123

# Ask questions
notebooklm notebook ask "My Research" "Summarize the key points"

# Generate content
notebooklm notebook audio "My Research" --format deep-dive --length medium
notebooklm notebook video "My Research" --style cinematic
notebooklm notebook slide "My Research" --format detailed

# Download artifacts
notebooklm notebook download "My Research" --format mp3 --output ./podcasts/
```

## Advanced Features

### Research Automation
```python
# Run web research with auto-import
research_notebook = client.research_web(
    query="latest developments in quantum computing",
    max_sources=10,
    mode="deep"  # or "fast"
)

# Run Drive research
drive_notebook = client.research_drive(
    folder_id="your-drive-folder-id",
    query="machine learning papers"
)
```

### Batch Operations
```python
# Import multiple sources at once
sources = [
    {"type": "url", "value": "https://example1.com"},
    {"type": "youtube", "value": "https://youtube.com/watch?v=..."},
    {"type": "file", "value": "./document.pdf"}
]

notebook.add_sources(sources)

# Generate multiple content types
formats = ["mp3", "mp4", "pdf", "png"]
for fmt in formats:
    notebook.download_artifacts(format=fmt, output_dir=f"./outputs/{fmt}")
```

### Custom Personas
```python
# Set a custom persona for more focused responses
notebook.set_persona(
    "You are a technical expert specializing in machine learning. "
    "Provide detailed, accurate explanations with code examples when relevant."
)
```

## Output Formats

### Audio Overview
- Formats: deep-dive, brief, critique, debate
- Lengths: short, medium, long
- Languages: 50+ supported
- Output: MP3/MP4

### Video Overview
- Formats: explainer, brief, cinematic
- Styles: 9 visual styles plus cinematic-video alias
- Output: MP4

### Slide Deck
- Formats: detailed, presenter
- Output: PDF, PPTX

### Infographic
- Orientations: 3 (portrait, square, landscape)
- Detail levels: 3 (low, medium, high)
- Output: PNG

### Quiz & Flashcards
- Configurable quantity and difficulty
- Output: JSON, Markdown, HTML

## Best Practices

1. **Error Handling**: The library uses undocumented Google APIs that may change - implement retry logic and fallback mechanisms
2. **Rate Limits**: Be mindful of usage quotas to avoid throttling
3. **Cleanup**: Temporary files are cleaned up automatically, but manage your output directories
4. **Authentication**: Uses your Google credentials - ensure you're logged in via browser auth flow
5. **Organization**: Create engagement-specific notebooks for different projects

## Updating the Skill

To update this skill to the latest version from the GitHub repository, follow these steps:

1. Clone or pull the latest version of the notebooklm-py repository:
   ```bash
   git clone https://github.com/teng-lin/notebooklm-py.git
   # or if you already have it:
   cd notebooklm-py && git pull
   ```

2. Re-run the installation process:
   ```bash
   pip install -e .  # for development mode, or just pip install notebooklm-py
   ```

3. If you're using the OpenClaw skill, you can update it by re-running the skill creation process from the latest repository.

## Troubleshooting

- If APIs break, check the [Troubleshooting guide](docs/troubleshooting.md) in the notebooklm-py repo
- For authentication issues, re-run the login process
- Rate limit errors require reducing request frequency or implementing exponential backoff
- Some features may require specific Google Workspace permissions

## Related Skills
- `ai-agent-development` - For building agents that utilize NotebookLM capabilities
- `audio-transcriber` - For processing generated audio content
- `video-frames` - For extracting frames from video overviews
- `app-builder` - For creating full applications around NotebookLM workflows

**Bet, Boss.** This skill puts the full power of NotebookLM at your fingertips. What notebook shall we create first? 😉