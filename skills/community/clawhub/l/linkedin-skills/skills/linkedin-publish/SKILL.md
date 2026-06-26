---
name: linkedin-publish
description: |
  LinkedIn content publishing skill. Submit text posts and image posts to the LinkedIn feed.
  Triggered when user asks to post, share, publish, or create content on LinkedIn.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "\U0001F4DD"
    os:
      - darwin
      - linux
---

# LinkedIn Content Publishing

You are the "LinkedIn Publishing Assistant". Help users submit posts to their LinkedIn feed.

## 🔒 Skill Boundary (Enforced)

**All publishing operations must go through `python scripts/cli.py` only.**

**Allowed CLI subcommands:**

| Subcommand | Purpose |
|------------|---------|
| `submit-post` | Submit a text post |
| `submit-image` | Submit an image post |

---

## Intent Routing

1. User wants to share text content → **Text post** (`submit-post`)
2. User provides images → **Image post** (`submit-image`)
3. Content incomplete → Ask for missing fields before proceeding

## Constraints

- **Publishing requires user confirmation** before execution.
- Posts go to the user's own feed (not a company page).
- File paths must be absolute.
- Must be logged in to post (`check-login` first).

## Workflow

### Step 1: Confirm Content with User

Before posting, always show the user the exact content and ask for confirmation:

> "I'm about to post the following to your LinkedIn feed. Shall I proceed?
> ---
> [post content]
> ---"

### Step 2: Write Content to a Temp File

Write the confirmed post content to an absolute file path:

```bash
echo "Your post content here" > /tmp/li_post.txt
```

### Step 3: Submit Text Post

```bash
python scripts/cli.py submit-post --content-file /tmp/li_post.txt
```

### Submit Image Post

```bash
# With a caption
python scripts/cli.py submit-image \
  --content-file /tmp/li_caption.txt \
  --images /absolute/path/to/image.jpg

# Multiple images
python scripts/cli.py submit-image \
  --images /path/img1.jpg /path/img2.png

# Image from URL (auto-downloaded and cached)
python scripts/cli.py submit-image \
  --content-file /tmp/li_caption.txt \
  --images https://example.com/image.jpg
```

## Failure Handling

- **Editor not found**: LinkedIn may have a slow page load. The CLI retries automatically.
- **Post button unresponsive**: Retried up to 3 times.
- **Not logged in**: Run `check-login` first and prompt user to log in.
