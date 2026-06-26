# Maintainer Publishing Notes

This file is for repository maintainers, not skill users.

## Preconditions

- Repository is clean and all docs are updated.
- CI workflows are green.
- `SKILL.md` metadata and version are correct.

## Publish flow

```bash
git add -A
git status
git commit -m "docs: update installation and setup guidance"
git push origin main
clawhub sync --all
```

## Release hygiene

- Keep `CHANGELOG.md` aligned with published version.
- Keep README examples aligned with script flags.
- Do not publish secrets or runtime state files.
