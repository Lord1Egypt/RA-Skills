---
name: notebooklm-content
description: Generate slides, audio overviews, and documents from sources using Google NotebookLM via browser automation. Use when the user wants to (1) create presentation slides from topics or sources, (2) generate audio explanations, (3) auto-produce NotebookLM content, or (4) build learning materials from text/URLs. Requires OpenClaw browser relay or Chrome remote debugging configured.
---

# NotebookLM Content Generator

Automated content generation workflow using Google NotebookLM.

## Prerequisites

- **OpenClaw Browser Relay** extension must be installed in Chrome
- Relay must be connected to local OpenClaw Gateway (default port 18792)
- User must be logged into NotebookLM in Chrome

## Quick Start

### 1. Ensure Browser Relay is Active

User action required:
1. Open Chrome with NotebookLM logged in
2. Click OpenClaw Browser Relay extension
3. Enable relay for the target tab

### 2. Basic Workflow

```
1. Navigate to NotebookLM
2. Create or open a notebook
3. Add sources (URLs, text, files)
4. Trigger content generation (slides/audio)
5. Wait for completion
6. Return shareable URL
```

## Commands

### Check Connection

```bash
openclaw browser status --browser-profile chrome-relay --json
```

### List Tabs

```bash
openclaw browser tabs --browser-profile chrome-relay --json
```

### Get Snapshot

```bash
openclaw browser snapshot --browser-profile chrome-relay --json --limit 120
```

### Navigate

```bash
openclaw browser open --url "https://notebooklm.google.com" --browser-profile chrome-relay
```

### Click Element

```bash
openclaw browser click <element-ref> --browser-profile chrome-relay --json
```

### Type Text

```bash
openclaw browser type <element-ref> "text content" --browser-profile chrome-relay --json
```

### Take Screenshot

```bash
openclaw browser screenshot --browser-profile chrome-relay
```

## Workflow: Generate Slides from Topic

1. **Open NotebookLM home**
   ```bash
   openclaw browser open --url "https://notebooklm.google.com" --browser-profile chrome-relay
   ```

2. **Create new notebook**
   - Find and click "ノートブックを新規作成" or "Create notebook"
   - Get snapshot to find element refs
   ```bash
   openclaw browser snapshot --browser-profile chrome-relay --json --limit 80
   ```

3. **Add sources**
   - Click "ソースを追加" or similar
   - For URLs: type URL and submit
   - For text: paste text content

4. **Generate slides**
   - Find "スライド資料" or "Slides" button in Studio panel
   - Click to start generation
   - Wait for "生成中..." to complete

5. **Get result URL**
   - Once complete, capture the notebook URL
   - Return shareable link to user

## Output Types

| Type | Japanese | Element Pattern |
|------|----------|-----------------|
| Slides | スライド資料 | button with "tablet" icon |
| Audio | 音声解説 | button with "audio_magic_eraser" icon |
| Video | 動画解説 | button with "subscriptions" icon |
| Mindmap | マインドマップ | button with "flowchart" icon |
| Report | レポート | button with "auto_tab_group" icon |
| Quiz | クイズ | button with "quiz" icon |

## Troubleshooting

### Element not found
- Run new snapshot: `openclaw browser snapshot --browser-profile chrome-relay --json`
- Element refs change on page updates

### Relay not connected
- Check Gateway status: `openclaw gateway status`
- User must enable relay in Chrome extension

### Generation stuck
- Wait longer (NotebookLM generation can take 1-3 minutes)
- Check for popups or dialogs

## Important Notes

- **Never hardcode element refs** - They change between sessions
- **Always get fresh snapshot** before clicking
- **User must keep Chrome open** during generation
- **Report progress** to user during long operations
