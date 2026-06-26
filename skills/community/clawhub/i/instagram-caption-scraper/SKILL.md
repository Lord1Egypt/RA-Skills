---
name: instagram-caption
description: Scrapes and returns the caption from any public Instagram post or reel URL. Use this when the user shares an Instagram link and wants to extract, read, summarise, translate, or analyse the caption of that post or reel.
version: 1.0.0
author: Raj
openclaw:
  emoji: "📸"
  requires:
    bins:
      - python3
    pip:
      - instaloader==4.14.1
---

# Instagram Caption Scraper

## Purpose
Extract the caption text from a public Instagram post or reel URL provided by the user.

## When to Use This Skill
Trigger this skill when the user:
- Shares an Instagram URL containing `/p/` or `/reel/`
- Says "get the caption", "what does this post say", "read this reel", "summarise this Instagram post"
- Wants to translate, rewrite, or analyse an Instagram caption

## How to Run

Execute the following shell command, replacing `{{url}}` with the Instagram URL:

```bash
python3 {{skill_dir}}/instagram_scraper.py {{url}}
```

The script will return one of:
- `CAPTION: <text>` — successfully extracted caption with metadata
- `ERROR: <reason>` — failure with explanation

## Example Triggers
- "Get the caption from https://www.instagram.com/p/DRiFkfoiIuC/"
- "What does this Instagram reel say? https://www.instagram.com/reel/ABC123/"
- "Summarise this post: https://www.instagram.com/p/XYZ/"
- "Translate this Instagram caption: https://www.instagram.com/p/ABC/"

## Output Format
On success the script returns:
```
CAPTION: <full caption text>

---
Owner   : @username
Type    : GraphImage / GraphVideo / GraphSidecar
Likes   : 1234
Shortcode: ABC123
```

## Rules
- Only trigger when a valid Instagram URL (`/p/` or `/reel/`) is present
- Never fabricate or guess caption content if the script returns an error
- If the post is private, inform the user and suggest they check the account's privacy settings
- Always display the full caption before offering any summary or analysis
- If the user asks to summarise or translate, do so AFTER displaying the raw caption

## Setup Notes
Requires Python 3.8+ and the `instaloader` library:
```bash
pip3 install instaloader==4.14.1
```
