# keelwright v1.8.1 — Wave 3: SKILL.md trim + version drift

Part of the 16-agent audit + meta-audit fix sequence (after v1.7.2, v1.8.0).

## What we improved
- **T34** — `SKILL.md` shrank from 11 598 → 1 606 lines (empty lines removed, all content/code-fences preserved). Much friendlier to Cursor/Claude Code context limits.
- **T40** — frontmatter `version` corrected to `1.8.0` (was stale `1.7.1`, caused version drift vs actual releases).
- Changelog now documents v1.7.2 / v1.8.0 / v1.8.1 honestly.

## Files changed
- `SKILL.md` (trimmed + version + changelog)
