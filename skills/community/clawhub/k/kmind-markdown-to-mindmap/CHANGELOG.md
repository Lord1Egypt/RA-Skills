# Changelog

All notable changes to this skill will be documented in this file.

## 0.1.1 - 2026-05-18

### Changed

- Clarified that the recommended input is a Markdown heading outline.
- Documented that non-heading body text is converted to node notes.
- Recommended PNG as the default image output format.
- Aligned image export guidance with the card-style node body layout where notes are shown as note icons.

## 0.1.0 - 2026-04-04

### Added

- Initial public release of the `kmind-markdown-to-mindmap` skill bundle.
- Offline conversion from Markdown outlines or plain text to KMind mind maps.
- Export support for `SVG`, `PNG`, and editable `.kmindz.svg`.
- Publish-safe theme, layout, and edge-route options for agent-facing usage.
- Bundled vendor CLI runtime under `scripts/vendor/`.
- Agent metadata under `agents/openai.yaml`.

### Notes

- Automatic `SVG` / `PNG` export requires a usable local Chromium browser.
- `.kmindz.svg` export does not depend on browser rendering.
