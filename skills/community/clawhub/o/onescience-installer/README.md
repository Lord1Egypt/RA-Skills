# OneScience Installer for ClawHub

This directory is a single-skill publish package for ClawHub.

## Included

- `SKILL.md`: published installer prompt
- `docs/domain-map.md`: domain mapping
- `docs/install-sequence.md`: recommended remote install sequence
- `.clawhubignore`: publish helper ignore rules

## Publish

```bash
clawhub skill publish ./clawhub/onescience-installer --slug onescience-installer --name "OneScience Installer" --version 0.1.0 --tags latest
```

## Notes

This package is intentionally lightweight and focuses on remote installation workflow, not on the whole knowledge base.
