# Changelog

All notable changes to the **hal-image** skill. Versioning follows SemVer.

This file starts at 1.1.0; earlier versions predate it.

## 1.1.0 — ClawHub metadata

- Frontmatter now declares `metadata.openclaw` with the binaries this skill
  actually drives (`magick`, `oxipng`) and a top-level `version`, which is what
  ClawHub's publish scanner reads.
- No change to behavior. Both tools remain fail-open per the skill's own
  contract: if one is missing, the original image passes through unchanged
  rather than the task being blocked.
