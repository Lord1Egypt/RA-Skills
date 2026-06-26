---
name: lark-doc-reviser
description: "Read unresolved comments in a Feishu (Lark) document and apply targeted edits block-by-block based on those comments. Use when the user shares a Feishu doc URL and asks to: (1) fetch/show document comments, (2) revise or edit the doc based on comments, (3) process feedback left in a Feishu doc. Requires lark-cli installed and authenticated."
---

# Lark Doc Reviser

## Workflow

### Step 1 — Fetch doc state

```bash
python3 scripts/fetch_doc.py <doc_url_or_token> --out workspace/<token>_state.json
```

This saves full doc state to `workspace/<token>_state.json` and prints a summary to stdout:
- `commented_blocks`: blocks that have unresolved comments, each with `elements`, `full_text`, and `comments[]{comment_id, anchor_text, instruction}`
- `all_blocks`: full block list (no elements, for structural reference)

**Always save to workspace.** The editing process may span multiple sessions.

### Step 2 — Present comments to user

Show each entry in `commented_blocks` as:

```
[block_type] full_text
  → 【anchor_text】 instruction
```

Ask the user to confirm which comments to address, or proceed if the intent is clear.

### Step 3 — Apply text edits

For each comment requiring a text change, construct a patches list and run:

```bash
python3 scripts/patch_blocks.py <doc_token> patches.json
```

`patches.json` format — **elements completely replace the block's existing content**:
```json
[
  {
    "block_id": "doxcnXXXX",
    "elements": [
      {"text": "普通文字"},
      {"text": "加粗", "bold": true},
      {"text": "代码", "code": true},
      {"text": "斜体", "italic": true}
    ]
  }
]
```

Supported element fields: `text` (required), `bold`, `italic`, `code`, `strikethrough`, `underline`.

**Note:** `update_text_elements` clears `comment_ids` from the elements. This is expected — always resolve addressed comments in Step 4.

### Step 4 — Resolve addressed comments

```bash
python3 scripts/resolve_comments.py <doc_token> <comment_id> [comment_id ...]
# or via stdin:
echo '["id1","id2"]' | python3 scripts/resolve_comments.py <doc_token> -
```

### Step 5 — Re-fetch and update state

Re-run Step 1 to refresh `workspace/<token>_state.json` after edits.

## Limitations

These operations are **not** handled by this skill's scripts and require additional API calls:

- **Insert blank line / empty block**: needs Create Block API
- **Delete a block** (e.g., remove a divider): needs Delete Block API
- **Structural reordering**: needs Move Block API

For such operations, use `lark-cli api` directly or ask the user if they want to handle them manually.

## Warning

Never use `lark-cli docs +update --mode replace_range --selection-by-title` to rename a heading. It selects the **entire section** (heading + all content until next heading) and deletes it all. Use `--selection-with-ellipsis "heading text"` instead.
