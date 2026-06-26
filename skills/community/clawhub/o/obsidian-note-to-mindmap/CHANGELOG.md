# Changelog

This file records user-visible changes for `obsidian-note-to-mindmap`.

## 0.1.0 - 2026-04-22

### Added

- Initial public release of the `obsidian-note-to-mindmap` wrapper skill.
- Thin Obsidian-to-KMind workflow that delegates conversion to the audited core skill `suka233/kmind-markdown-to-mindmap`.
- Explicit first-install confirmation flow for the audited core skill.
- Narrow safety boundaries: no vault scan, no hidden installs, no note mutation.

### Notes

- First-time core-skill installation requires the `clawhub` CLI and network access.
- Actual map generation runtime requirements are defined by the audited core skill.
