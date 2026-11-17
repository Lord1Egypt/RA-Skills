# GitHub Issue Template for KB Template Updates

## Standard Title Format

```
docs: add <languages> translations to <template-name> (<version>)
```

Examples:
- `docs: add French & Korean translations to common-responses (v1.1)`
- `docs: add Japanese translation to common-responses (v1.2)`

## Labels

- `documentation`
- `i18n`
- `customer-service` (if applicable)

## Body Template

See `scripts/build-issue-body.sh` for auto-generation. Manual template:

```markdown
## 📝 Template Update: <version>

**Date:** YYYY-MM-DD
**File:** `kb-templates/<file>.md`
**Languages added:** <languages>

### Changes
- Added translations for **<languages>** across all template categories
- Categories covered: <list>
- Version bumped to **<version>**

### Feishhu Wiki
<wiki-url>

### Checklist
- [x] Local template updated
- [x] Changelog updated
- [x] Synced to Feishu Wiki
- [ ] Reviewed by native speaker
- [ ] Committed and pushed
```
