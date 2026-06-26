# Changelog

All notable changes to **best-image-generation** are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.2] — 2026-05-16

### Added
- `README.md` with quick-start, trigger table, and output protocol.
- `CHANGELOG.md`.
- `examples/basic.md` — minimal text-to-image walkthrough.
- `examples/advanced.md` — multi-image edit, mask inpainting, and 4K size selection.
- `version` and `tags` fields in `SKILL.md` frontmatter for better ClawHub search ranking.

### Changed
- No behavioral changes — purely documentation & metadata polish for the ClawHub listing.

---

## [1.0.1] — 2026-05-16

### Fixed
- Filename sanitization step before shell interpolation (defense against prompt-injected filenames).
- Extension whitelist enforcement (`.png / .jpg / .jpeg / .webp`).

---

## [1.0.0] — 2026-05-16

### Added
- Initial public release.
- Text-to-image via `POST /v1/images/generations` (`application/json`).
- Image edit / image-to-image via `POST /v1/images/edits` (`multipart/form-data`), including optional mask for inpainting and up to 16 reference images per call.
- Synchronous base64 response handling — `data[i].b64_json` decoded and written to disk as `wellapi-<TIMESTAMP>.<ext>`.
- `MEDIA:<absolute_path>` stdout protocol for OpenClaw auto-attach.
- Reference implementations:
  - `references/python.md` (zero-dependency, all platforms)
  - `references/powershell.md` (Windows, PS 5.1+)
  - `references/curl_heredoc.md` (Unix/macOS)
- Chinese & English triggers (`高质量生图：…` / `编辑图片：…` / `best image: …` / `edit image: …`).
- Size presets from `1024×1024` through 4K (`3840×2160`, `2160×3840`), with custom-size validation rules.
- Quality / format / background / moderation knobs surfaced on the edit endpoint.
