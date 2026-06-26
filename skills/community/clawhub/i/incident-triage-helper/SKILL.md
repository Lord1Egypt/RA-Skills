---
name: local-skill-package-publisher
version: 0.2.0
description: Complete local skill package to assess and potentially publish.
license: MIT
---

# Local Skill Package Publisher

This package contains everything needed to review, validate, and prepare a skill for publishing.

## Included files

- `SKILL.md` - package metadata and usage notes
- `docs/review-checklist.md` - review steps before publication
- `examples/sample-skill.md` - example skill structure
- `templates/publish-request.md` - publication request template
- `scripts/validate.sh` - local validation helper

## Validation

Run:

```bash
./scripts/validate.sh
```

## Publishing checklist

1. Confirm metadata is complete.
2. Validate required files exist.
3. Review examples and supporting docs.
4. Package for handoff or publication.
