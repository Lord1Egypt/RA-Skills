---
name: multilingual-kb-update
description: Add new language translations to customer service knowledge base templates, sync to Feishu Wiki, and create a GitHub issue to document the change. Use when asked to translate/add languages to KB templates, update multilingual customer service response templates, or run the multilingual KB update workflow end-to-end.
---

# Multilingual KB Template Update

End-to-end workflow for adding languages to customer service KB templates and propagating changes.

## Workflow

### 1. Update the local template file

1. Read `kb-templates/common-responses.md` (or the target file).
2. For each existing template section, add a new subsection per requested language using the format:
   ```
   ### 🇫🇷 Français
   <translated text>
   ```
3. Add the language flag + name to the "Supported languages" line in the header.
4. Append a row to the Changelog table with date and summary.
5. Save the file.

**Translation quality:**
- Match the tone of the source (formal/professional for CS).
- Use locale-appropriate conventions (e.g., French punctuation with non-breaking spaces where required; Korean honorifics).
- Keep placeholders, links, and formatting intact.

### 2. Sync to Feishu Wiki

Use the Feishu/Lark Open API to update the Wiki document.

**Prerequisites (env vars):**
- `FEISHU_APP_ID` — Feishu custom app ID
- `FEISHU_APP_SECRET` — Feishu app secret
- `FEISHU_WIKI_SPACE_ID` — target Wiki space ID
- `FEISHU_WIKI_NODE_TOKEN` — target document node token

**Steps:**

```bash
# 1. Get tenant access token
TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$FEISHU_APP_ID\",\"app_secret\":\"$FEISHU_APP_SECRET\"}" \
  | jq -r '.tenant_access_token')

# 2. Get the document ID from the wiki node
DOC_ID=$(curl -s -X GET "https://open.feishu.cn/open-apis/wiki/v2/spaces/$FEISHU_WIKI_SPACE_ID/nodes/$FEISHU_WIKI_NODE_TOKEN" \
  -H "Authorization: Bearer $TOKEN" | jq -r '.data.node.obj_token')

# 3. Get existing document blocks (to find where to append)
#    Then create new blocks with the translated content.
#    See references/feishu-api.md for block creation details.
```

For full block creation payloads, read `references/feishu-api.md`.

If Feishu credentials are not configured, report this clearly and skip the sync step — do not fail the entire workflow.

### 3. Create a GitHub issue

**Prerequisites:**
- `gh` CLI installed and authenticated (`gh auth status`), OR
- `GITHUB_TOKEN` env var with repo scope

```bash
gh issue create \
  --repo "$GITHUB_REPO" \
  --title "docs(kb): add $LANGUAGES translations to common-responses" \
  --body "$(cat <<EOF
## Summary
Added $LANGUAGES translations to \`kb-templates/common-responses.md\`.

## Changes
- Added $LANGUAGES versions for all template sections
- Updated header language list
- Updated changelog

## Files
- \`kb-templates/common-responses.md\`

## Sync Status
- [ ] Feishu Wiki updated
- [ ] Local file committed
EOF
)"
```

If `gh` is not available, use the GitHub REST API directly with `curl`:

```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$GITHUB_REPO/issues" \
  -d "{\"title\":\"...\",\"body\":\"...\"}"
```

If GitHub credentials are not configured, output the issue title and body as markdown so the user can create it manually.

### 4. Commit locally

```bash
git add kb-templates/common-responses.md
git commit -m "docs(kb): add $LANGUAGES translations to common-responses"
```

Do not push unless explicitly asked.

## Configuration Reference

Store these in `TOOLS.md` or as environment variables:

| Variable | Purpose |
|----------|---------|
| `FEISHU_APP_ID` | Feishu app ID |
| `FEISHU_APP_SECRET` | Feishu app secret |
| `FEISHU_WIKI_SPACE_ID` | Wiki space ID |
| `FEISHU_WIKI_NODE_TOKEN` | Wiki document node token |
| `GITHUB_REPO` | Target repo (e.g., `org/repo`) |
| `GITHUB_TOKEN` | GitHub PAT with repo scope |

## Language Reference

| Language | Flag | Code |
|----------|------|------|
| Chinese (Simplified) | 🇨🇳 | zh-CN |
| English | 🇬🇧 | en |
| French | 🇫🇷 | fr |
| Korean | 🇰🇷 | ko |
| Japanese | 🇯🇵 | ja |
| German | 🇩🇪 | de |
| Spanish | 🇪🇸 | es |
| Portuguese (Brazil) | 🇧🇷 | pt-BR |
| Russian | 🇷🇺 | ru |
| Arabic | 🇸🇦 | ar |
