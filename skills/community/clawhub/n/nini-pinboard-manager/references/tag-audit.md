# Tag Audit Mode

Audit all bookmarks against the tag convention, present issues in batches, and apply fixes with user confirmation.

Reference: `~/.config/nini-skill/pinboard-manager/tag-convention.md` (generated during first-time setup)

## Step 1: Fetch all bookmarks

```bash
curl -s "https://api.pinboard.in/v1/posts/all?auth_token=$PINBOARD_AUTH_TOKEN&format=json" > /tmp/pinboard_all.json
```

Parse the JSON and count total bookmarks.

## Step 2: Analyze tag issues

Load the tag convention from `~/.config/nini-skill/pinboard-manager/tag-convention.md` and scan all bookmarks. Categorize issues:

| Priority | Category | Example |
|----------|----------|---------|
| 1 | Typos | `ainme` -> `anime` |
| 2 | Missing tags | Bookmarks with empty `tags` field |
| 3 | Case issues | `Health` -> `health` |
| 4 | Chinese tags | `终极文档` -> `reference` |
| 5 | Concept overlap | `ai` + `llm` on same bookmark |
| 6 | Deprecated tags | `TODO`, year tags like `2025` |

## Step 3: Present issues in batches

For each category (in priority order), present **5-10 bookmarks per batch**:

```text
### Batch 1: Typos (3 items)

1. 「Some anime article」
   URL: https://example.com/anime
   Current tags: `ainme game`
   Suggested: `anime game`

2. 「Editor comparison」
   URL: https://example.com/editor
   Current tags: `editer tool`
   Suggested: `programming tool`

3. ...

Options: [confirm all] [modify] [skip all] [skip individual]
```

## Step 4: Apply confirmed changes

For each confirmed change, update via `/posts/add` with `replace=yes`:

```bash
# URL-encode all parameters
curl -s "https://api.pinboard.in/v1/posts/add?auth_token=$PINBOARD_AUTH_TOKEN&format=json&url=ENCODED_URL&description=ENCODED_TITLE&extended=ENCODED_NOTES&tags=NEW_TAGS&shared=ORIGINAL_SHARED&toread=ORIGINAL_TOREAD&replace=yes"
sleep 3  # Rate limit
```

**IMPORTANT**: Preserve ALL original fields. Only modify `tags`.

## Step 5: Summary

After all batches are processed, show:

```text
Tag Audit Complete
- Bookmarks scanned: 200
- Issues found: 45
- Fixed: 38
- Skipped: 7
```
