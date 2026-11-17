---
name: lark-to-anything
description: >
  Use when the user provides a Feishu/Lark document URL (feishu.cn or
  larksuite.com) and wants to export, download, save, or convert it to a
  local Markdown file. Triggers on phrases like "把飞书文档导出成 markdown"、
  "保存到本地"、"转成 md 文件", or any feishu.cn/docx link with export intent.
---

# lark-to-anything: Feishu Doc → Local Markdown

Export any Feishu document to a self-contained local folder:
`<doc-title>/index.md` + `<doc-title>/assets/` with all images downloaded.

## Prerequisites

Read `../lark-shared/SKILL.md` for auth and global flags before running any
`lark-cli` command.

## Steps

### 0. Check lark-cli version

```bash
lark-cli --version
```

If below `1.0.66`, stop and tell the user:

> 画板缩略图需要 lark-cli ≥ 1.0.66，当前版本是 X.X.X，请先升级：
> ```
> npm install -g @larksuite/cli@1.0.66 && npx skills add larksuite/cli -y -g
> ```
> 升级完成后请重启 Claude Code，然后重新执行导出。

### 1. Fetch the document

```bash
lark-cli docs +fetch \
  --api-version v2 \
  --doc "<URL or token>" \
  --doc-format markdown \
  --format json > /tmp/lark_fetch.json
```

### 2. Convert, download assets, and save

The conversion script is bundled with this skill. Run it with:

```bash
python3 "$(dirname "$0")/scripts/to_markdown.py" /tmp/lark_fetch.json
```

Or use the full skill path (replace `<skills-dir>` with your skills directory,
typically `~/.claude/skills`):

```bash
python3 <skills-dir>/lark-to-anything/scripts/to_markdown.py /tmp/lark_fetch.json
```

The script:
- Creates `<cwd>/<doc-title>/index.md`
- Downloads all images into `<doc-title>/assets/` concurrently (stdlib only, no pip)
- Downloads whiteboard thumbnails via `lark-cli docs +media-download --type whiteboard`
- Rewrites all image links to relative local paths
- Fails gracefully: failed images keep original URL, failed whiteboards keep placeholder

Pass `--output-dir <path>` to save somewhere other than cwd.

### 3. Report back

Tell the user the path to `index.md` and the asset counts.

## Output structure

```
<doc-title>/
  index.md          ← converted document with local image references
  assets/
    image-1.png
    whiteboard-1.png
    ...
```

## Element conversion table

| Feishu element | Markdown result |
|---|---|
| `<title>` | `# Title` at top |
| `<callout>` | `>` blockquote |
| `<table>` HTML | standard markdown table |
| `<cite type="user">` | `@DisplayName` |
| `<cite type="doc">` | `[Document Title]` |
| `<checkbox>` | `- [ ]` / `- [x]` |
| Images (any location) | downloaded → `assets/image-N.ext` |
| `<whiteboard>` | downloaded thumbnail → `assets/whiteboard-N.png` |
| `<figure>/<source>` | `> *[附件: filename]*` |
| `<readonly-block>` | removed |

## Error handling

- **Permission denied**: use `--as user`; document must be accessible to the logged-in user.
- **Image download fails**: Feishu image URLs expire. Re-run the fetch to get fresh URLs.
- **Whiteboard fails**: upgrade lark-cli to ≥ 1.0.66 (see Step 0).
- **Large documents**: pass `--scope section` or `--scope keyword` — see `../lark-doc/references/lark-doc-fetch.md`.

