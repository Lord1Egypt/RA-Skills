---
name: gmail-link-archiver
version: 1.1.0
description: >-
  Connects to Gmail via IMAP, filters emails by subject prefix keyword in a
  specified mailbox, crawls links found in filtered emails using Playwright
  (to bypass bot detection), converts crawled content to Markdown, and saves
  it to the OpenClaw workspace. Use when the user wants to archive web content
  from email links, save newsletter links as Markdown, or crawl URLs from
  filtered emails.
allowed-tools: Bash(python3:*), Bash(python:*), Bash(pip:*), Bash(pip3:*), Bash(bash:*), Bash(chmod:*), Bash(mkdir:*), Bash(cat:*), Bash(ls:*)
metadata: >-
  {"openclaw":{"emoji":"📬","requires":{"bins":["python3"],"env":[]},"install":[{"id":"setup","kind":"bash","command":"bash references/setup.sh","label":"Install dependencies (Playwright + html2text)"}]}}
---

# Gmail Link Archiver

Archive web content from your email links. This skill connects to Gmail via IMAP, filters emails by a subject prefix keyword, crawls every link using Playwright (headless Chromium), converts pages to Markdown, and saves them to your OpenClaw workspace.

## Quick Start

### 1. Install dependencies (one-time)

```bash
bash references/setup.sh
```

This automatically installs:
- `playwright` (Python) + Chromium browser binary
- `html2text` for HTML→Markdown conversion

### 2. First run — interactive setup

```bash
python3 references/gmail_link_archiver.py
```

The first run will prompt you for:

| Setting | Description | Default |
|---------|-------------|---------|
| IMAP server | Gmail IMAP host | `imap.gmail.com` |
| IMAP port | SSL port | `993` |
| Gmail address | Your full email address | — |
| App password | Gmail App Password (NOT your regular password) | — |
| Default mailbox | IMAP folder to search | `INBOX` |
| Subject prefix | Filter emails whose subject starts with this | — |
| Workspace path | Where to save Markdown files | `~/openclaw-workspace/mail-archive` |

Credentials are saved locally to `~/.config/gmail-link-archiver/config.json` with `0600` permissions. They are **never transmitted or logged**.

> **Gmail App Password**: You need to generate an App Password at
> https://myaccount.google.com/apppasswords (requires 2FA enabled).

### 3. Subsequent runs

After the first setup, subsequent runs will read credentials from the saved config:

```bash
# Use saved config defaults
python3 references/gmail_link_archiver.py

# Override mailbox and prefix on the fly
python3 references/gmail_link_archiver.py --mailbox "INBOX" --subject-prefix "[Newsletter]"

# Save to a different workspace
python3 references/gmail_link_archiver.py --workspace ~/my-archive

# Limit number of links to crawl
python3 references/gmail_link_archiver.py --max-links 10

# Re-run the setup interview
python3 references/gmail_link_archiver.py --reconfigure
```

## How It Works

1. **Connect** — Authenticates to Gmail via IMAP SSL
2. **Filter** — Searches the specified mailbox for emails matching the subject prefix
3. **Extract** — Parses email bodies (HTML + plain text) to find HTTP/HTTPS links
4. **Crawl** — Opens each link in headless Chromium via Playwright (bypasses bot detection, renders JavaScript)
5. **Convert** — Transforms the crawled HTML into clean Markdown with metadata headers
6. **Save** — Writes each Markdown file to the workspace directory

## Pipeline Diagram

```
Gmail IMAP ──► Filter by Subject ──► Extract Links
                                          │
                                          ▼
                         Playwright + Chromium (headless)
                                          │
                                          ▼
                              HTML → Markdown (html2text)
                                          │
                                          ▼
                           Save to OpenClaw Workspace
```

## CLI Reference

```
usage: gmail_link_archiver.py [-h] [--mailbox MAILBOX]
                               [--subject-prefix PREFIX]
                               [--workspace PATH]
                               [--max-links N]
                               [--reconfigure]

Options:
  --mailbox, -m        IMAP mailbox to search (default: from config)
  --subject-prefix, -s Subject prefix to filter emails
  --workspace, -w      Directory to save Markdown files
  --max-links          Max number of links to crawl (default: 50)
  --reconfigure        Re-run the setup interview
```

## Output Format

Each crawled page is saved as a Markdown file with YAML frontmatter:

```markdown
---
source: https://example.com/article
crawled_at: 2026-03-27T12:00:00Z
---

# Article Title

Article content converted to clean Markdown...
```

Files are named using a sanitized version of the URL plus a short hash for uniqueness.

## Example Usage with Claude

Ask Claude to run the archiver:

> "Run the Gmail Link Archiver to crawl links from my emails with subject starting with '[ReadLater]'"

Claude will execute:

```bash
python3 references/gmail_link_archiver.py --subject-prefix "[ReadLater]"
```

Or to set up fresh:

> "Set up the Gmail Link Archiver with my credentials"

```bash
python3 references/gmail_link_archiver.py --reconfigure
```

## Troubleshooting

**"App password" rejected?**
- Ensure 2-Step Verification is enabled on your Google account
- Generate a new App Password at https://myaccount.google.com/apppasswords
- Use the 16-character password without spaces

**Playwright/Chromium issues?**
```bash
# Reinstall Chromium
python3 -m playwright install chromium
# Install system dependencies (Linux)
sudo python3 -m playwright install-deps chromium
```

**No emails found?**
- Check the mailbox name (use `INBOX`, `[Gmail]/All Mail`, etc.)
- Verify the subject prefix matches exactly (case-sensitive)
- Try a broader prefix

**Permission denied on config file?**
```bash
chmod 600 ~/.config/gmail-link-archiver/config.json
```

## Security

- Credentials are stored locally at `~/.config/gmail-link-archiver/config.json`
- File permissions are set to `0600` (owner read/write only)
- Credentials are **never** transmitted anywhere except to the IMAP server
- Credentials are **never** logged or printed to stdout
- Use Gmail App Passwords (not your main Google password)
- The config directory has `0700` permissions

## Requirements

- Python 3.8+
- Linux (Ubuntu/Debian) for MVP
- Gmail account with IMAP enabled and App Password
- Internet connection for IMAP and web crawling
