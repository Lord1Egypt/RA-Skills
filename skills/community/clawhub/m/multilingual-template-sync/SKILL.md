---
name: multilingual-template-sync
description: Add new language translations to customer service response templates and sync the update across Feishu Wiki, GitHub, and local files. Use when asked to (1) add translations to kb-templates/common-responses.md or similar multilingual template files, (2) sync template changes to Feishu Wiki customer service knowledge base, (3) create GitHub issues documenting template updates, or (4) perform the full multilingual template update pipeline.
---

# Multilingual Template Sync

End-to-end workflow for adding languages to customer service response templates and propagating the change across all destinations.

## Prerequisites

- **Feishu**: App credentials (`FEISHU_APP_ID`, `FEISHU_APP_SECRET`) and target Wiki space/node token. The Feishu plugin must be enabled in OpenClaw config, or use the Feishu Open API directly via `scripts/feishu_wiki_sync.sh`.
- **GitHub**: `gh` CLI authenticated, or `GITHUB_TOKEN` env var with repo scope.
- **Template file**: Default path is `kb-templates/common-responses.md` in the workspace.

## Workflow

### 1. Add Translations

1. Read the existing template file to understand structure (sections per scenario, one block per language).
2. For each new language, append a translated block under every existing section.
3. Use native-speaker-quality translations. For French use formal "vous"; for Korean use 하십시오체 (formal polite).
4. Update the header "Last updated" date and the Changelog table.
5. Save the file.

See `references/language-style-guide.md` for per-language tone and formatting rules.

### 2. Sync to Feishu Wiki

Run the sync script with the target Wiki node token:

```bash
bash scripts/feishu_wiki_sync.sh \
  --file kb-templates/common-responses.md \
  --space <FEISHU_SPACE_ID> \
  --node <FEISHU_NODE_TOKEN>
```

The script obtains a tenant access token, converts Markdown to Feishu Docx blocks, and creates/updates the Wiki document.

If the Feishu plugin is enabled in OpenClaw, alternatively use the plugin's document API.

### 3. Create GitHub Issue

```bash
bash scripts/github_issue.sh \
  --repo owner/repo \
  --title "docs: add <languages> translations to common-responses" \
  --body-file /tmp/issue-body.md
```

The issue body should include:
- Summary of languages added
- Number of template sections translated
- Feishu Wiki sync status
- Changelog entry

### 4. Commit Local Changes

```bash
git add kb-templates/common-responses.md
git commit -m "docs: add <languages> translations to common-responses (v<version>)"
```

## Quick Reference

| Step | Command/Action |
|------|---------------|
| Add languages | Edit template file directly |
| Feishu sync | `bash scripts/feishu_wiki_sync.sh ...` |
| GitHub issue | `bash scripts/github_issue.sh ...` |
| Git commit | `git add && git commit` |

## Tips

- Always translate every section; partial translations cause confusion.
- After Feishu sync, verify the document renders correctly in the Wiki UI.
- Tag the GitHub issue with `documentation` and `i18n` if labels exist.
- For bulk language additions, consider using an LLM to draft translations, then review for accuracy.
