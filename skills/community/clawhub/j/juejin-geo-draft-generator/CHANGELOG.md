# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-12

### Added
- Initial release of the `juejin-geo-draft-publisher` Skill.
- Implemented core prompt pipeline for rewriting brand assets into Juejin developer-style articles.
- Added `/prompts/` directory including intake, content_reader, juejin_rewrite, markdown_formatter, tags_generator, and quality_check.
- Added output templates for article, summary, and publish checklist.
- Provided local Playwright automation script (`draft_to_juejin.example.py`) strictly limited to draft creation.
- Created `examples/` directory featuring PowerMatrix / OpenClaw use case.
- Added documentation: `SKILL.md`, `README.md`, and automation safety guidelines.
