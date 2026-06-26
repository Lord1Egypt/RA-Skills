# Setup Guide

## Prerequisites

Install the following tools before using notes-know-you:

### 1. Python 3.9+
```bash
python --version
```

### 2. pandoc (required for HTML → Markdown conversion)

**macOS:**
```bash
brew install pandoc
```

**Windows:**
Download from https://pandoc.org/installing.html or:
```bash
winget install JohnMacFarlane.Pandoc
```

**Linux:**
```bash
sudo apt install pandoc   # Debian/Ubuntu
sudo dnf install pandoc   # Fedora
```

### 3. evernote-backup
```bash
pip install evernote-backup
```

### 4. beautifulsoup4 + lxml (used by the conversion script)
```bash
pip install beautifulsoup4 lxml
```

---

## First-Time Evernote Setup

### Step 1 — Create the local database

**Yinxiang (China users):**
```bash
python -m evernote_backup init-db --backend china -d "path/to/en_backup.db"
```

**International Evernote:**
```bash
python -m evernote_backup init-db -d "path/to/en_backup.db"
```

### Step 2 — Authenticate

**Option A: Password login** (may not work for some accounts):
The tool will prompt for username and password interactively.

**Option B: Developer Token** (recommended):
1. Log into Evernote/Yinxiang in your browser
2. Visit the token page:
   - Yinxiang: `https://app.yinxiang.com/api/DeveloperToken.action`
   - International: `https://www.evernote.com/api/DeveloperToken.action`
3. Create a token, then run:
   ```bash
   python -m evernote_backup init-db --backend china -d "path/to/en_backup.db" -t "YOUR_TOKEN"
   ```

### Step 3 — Set environment variables

Add to your shell profile (`.bashrc`, `.zshrc`) or system environment:

```bash
export NOTES_DB_PATH="/path/to/en_backup.db"
export NOTES_BACKEND="china"          # omit for international
export NOTES_TOKEN="your_token_here"  # optional
```

Windows (PowerShell profile or System Properties):
```powershell
$env:NOTES_DB_PATH = "F:\notes\en_backup.db"
$env:NOTES_BACKEND = "china"
```

---

## Updating an Expired Token

If your token expires:
```bash
python -m evernote_backup reauth -d "path/to/en_backup.db" -t "NEW_TOKEN"
```

---

## Rate Limiting

If you see `CRITICAL: Rate limit reached`, the Evernote API has throttled you.
Wait 25–30 minutes, then retry. The tool resumes from where it left off — no need
to start over.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `pandoc: command not found` | Install pandoc (see above) |
| `ModuleNotFoundError: bs4` | `pip install beautifulsoup4` |
| `ModuleNotFoundError: lxml` | `pip install lxml` |
| Auth fails after token set | Token may have expired — generate a new one |
| Export produces empty `.enex` | Run sync first: `python -m evernote_backup sync` |
