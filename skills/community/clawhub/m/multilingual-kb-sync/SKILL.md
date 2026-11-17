---
name: multilingual-kb-sync
description: >
  Add new language translations to customer service response templates and sync them across
  Feishu Wiki, GitHub, and local files. Use when: (1) adding new languages to KB templates,
  (2) updating multilingual customer service responses, (3) syncing template changes to
  Feishu Wiki knowledge base, (4) creating GitHub issues to document template updates,
  (5) running the full multilingual template update pipeline. Triggers on phrases like
  "add language", "translate template", "sync to wiki", "update customer service templates",
  "多语言模板", "新增语种", "同步知识库".
---

# Multilingual KB Template Sync

End-to-end workflow for adding language translations to customer service templates and
publishing changes across all channels.

## Prerequisites

- **Feishu App credentials**: Set `FEISHU_APP_ID` and `FEISHU_APP_SECRET` env vars, or
  configure the `feishu` plugin in OpenClaw config with wiki access.
- **GitHub CLI**: `gh auth login` completed, or `GITHUB_TOKEN` env var set.
- **clawhub CLI**: Installed (`npm i -g clawhub`) for skill publishing.

## Workflow

### 1. Update Local Template

Read the target template file (e.g., `kb-templates/common-responses.md`).

For each new language, add a section under every existing category:

```markdown
### 🇫🇷 Français
<translated text>

### 🇰🇷 한국어
<translated text>
```

Maintain the existing structure — same categories, same ordering, one language block per
language. Use native speaker-quality translations; do not rely on machine translation
without review for customer-facing content.

Update the **Changelog** table at the bottom with date, version bump, and description.

### 2. Sync to Feishu Wiki

Run the sync script:

```bash
bash scripts/sync-feishu-wiki.sh <file-path> <wiki-space-id> <parent-node-token>
```

The script:
1. Obtains a tenant access token from Feishu OAuth
2. Creates or updates a wiki document under the specified parent node
3. Converts markdown to Feishu docx blocks via the API
4. Returns the document URL

If the document already exists (matched by title), it updates it instead of duplicating.

**Configuration:**
- `FEISHU_APP_ID` / `FEISHU_APP_SECRET` — required
- `FEISHU_WIKI_SPACE_ID` — default wiki space (can override per call)

### 3. Create GitHub Issue

Run:

```bash
bash scripts/create-github-issue.sh <repo> <title> <body-file>
```

Or use `gh` directly:

```bash
gh issue create --repo <owner/repo> \
  --title "docs: add French & Korean translations to common-responses" \
  --body-file <(scripts/build-issue-body.sh)
  --label "documentation" --label "i18n"
```

The issue body should include:
- Summary of languages added
- List of categories updated
- Changelog entry
- Link to Feishu Wiki document (if available)

### 4. Commit & Push (if repo exists)

```bash
git add kb-templates/
git commit -m "docs: add French & Korean translations to common-responses (v1.1)"
git push
```

## File Structure Convention

```
kb-templates/
├── common-responses.md        # Main template file
└── <other-templates>.md
```

Each template uses this per-category pattern:

```markdown
## <N>. <Category Name> / <English Name>

### 🇨🇳 中文
<Chinese text>

### 🇺🇸 English
<English text>

### 🇫🇷 Français
<French text>

### 🇰🇷 한국어
<Korean text>
```

## Adding More Languages Later

1. Read the existing template file
2. Add a new `### <flag> <language>` block under each category
3. Bump version in changelog
4. Re-run steps 2–4 above

## References

- **Feishu Wiki API**: See [references/feishu-wiki-api.md](references/feishu-wiki-api.md)
  for endpoint details and block format conversion.
- **GitHub Issue Templates**: See [references/github-issue-template.md](references/github-issue-template.md)
  for standard issue format.
