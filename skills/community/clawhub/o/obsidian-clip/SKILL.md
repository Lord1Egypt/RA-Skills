---
name: obsidian-clip
description: Create and manage Obsidian “Clip” notes (web/article/page clips). Use when the user says “clip/剪藏/收藏/保存这个链接”, wants a readable summary of a URL, and wants it saved into an Obsidian vault under Clip/YYYY-MM/.
---

# Obsidian Clip

Turn a URL into a **readable, reusable Clip note** in an Obsidian vault.

## Storage

- Vault: `${OBSIDIAN_VAULT}` (recommended to set; fallback supported by script)
- Folder: `Clip/YYYY-MM/`
- Filename: `YYYY-MM-DD_标题_关键词.md`

## Output standard (must follow)

The skill supports **Chinese and English** notes.

- Default language: **auto-detect** (based on your system locale and whether the content contains CJK characters)
- Override language: set `OBSIDIAN_CLIP_LANG=zh` or `OBSIDIAN_CLIP_LANG=en`

Structure:

1) **Theme / 主题一句话** (1 sentence, plain)
2) **Takeaways / 要点** (5–10 bullets, each ≤ 1 line)
3) **How I’ll use it / 我怎么用** (1–3 bullets; actions / why it matters)
4) **Limits / 规则/限制** (optional; paywall/login required, license, caveats)

## Workflow

1) **Fetch the page**
   - Prefer lightweight extraction tools (e.g., `web_fetch`) first.
   - Use a real browser only when needed (JS-heavy sites / WeChat / login / extraction fails).
   - If blocked by login/paywall, ask the user to log in, then retry.
2) **Rewrite for readability**
   - Don’t make the output about tool limitations.
   - If details are still inaccessible, produce a useful clip anyway: page定位 + 可用信息 + what you need to finish.
   - Do **not** send screenshots/images unless the user explicitly requests.
3) **Save to Obsidian** using the bundled script.

## Bundled script

Path: `scripts/clip_save.sh`

Example:

```bash
bash scripts/clip_save.sh \
  --url "https://example.com" \
  --title "页面标题" \
  --theme "一句话主题" \
  --bullets "要点1" --bullets "要点2" \
  --actions "我怎么用1" \
  --limits "规则/限制（可选）" \
  --tags "clip" --tags "ai" \
  --keywords "keyword1-keyword2" \
  --date "YYYY-MM-DD"
```

Notes:
- `--bullets` / `--actions` / `--limits` / `--tags` can be repeated.
- Keep `--keywords` short (2–5 tokens joined by `-`).
