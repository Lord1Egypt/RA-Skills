# Changelog

## [0.2.1] - 2026-05-28
Rewrote frontmatter description to concise 200–500 character format for improved agent-trigger clarity.

## [0.2.0] - 2026-05-28

### Changed
- Replaced dual-mode obsidian CLI + obsidian-headless with `notesmd-cli` as the sole interface
- `notesmd-cli` works without Obsidian installed (server/VPS environments)
- Vault setup now uses `notesmd-cli add-vault` instead of manual config file parsing
- Daily note appending uses `notesmd-cli daily --content` (auto-reads daily notes config)
- Removed Obsidian Sync dependency (`obsidian-headless` required a paid subscription)

### Removed
- `references/obsidian-headless.md`
- `references/obsidian-cli.md` (replaced by `references/notesmd-cli.md`)

## [0.1.0] - 2026-05-28

### Added
- Initial release: obsidian-vault-writer skill
- Desktop mode via `obsidian` CLI (`daily:append`, `create`)
- Headless mode: direct file writes to vault directory with vault path auto-detection
- Optional Obsidian Sync via `obsidian-headless` (see `references/obsidian-headless.md`)
- Content format for X post drafts (called from x-post-strategist)
- References: obsidian-cli, obsidian-markdown, obsidian-canvas, obsidian-bases, obsidian-headless
