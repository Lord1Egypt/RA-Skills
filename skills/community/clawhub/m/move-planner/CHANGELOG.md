# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] — 2026-06-08

### Added
- **Privacy and Data Handling** section in SKILL.md describing assistant-mediated reads/writes against the local `move-data.json` file, with an explicit refused-data list (SSNs, full account numbers, mortgage application materials, full ID numbers)
- **Permissions and Privacy** section in README.md so users see the scope of access (local file only, no external tool calls, refused data categories) before installing

### Changed
- Narrowed the activation triggers in the `description` frontmatter to require explicit move context (named addresses/dates/vendors), with a "do NOT trigger" guardrail for casual mentions of moving, unrelated real estate browsing, or generic packing questions
- Unquoted the `version` field in frontmatter (matches updated ClawHub CLI semver requirements)

## [1.0.1] — 2026-05-13

### Changed
- Frontmatter `version` field now quoted as a string per ClawHub CLI requirements
- Added this CHANGELOG.md for consistency with the rest of the published skill catalog

### Notes
- No behavior changes in this release. Purely documentation and metadata cleanup.

## [1.0.0] — 2026-04-12

### Added
- Initial release
- Full residential move management: timelines, packing, movers, utilities, address changes, school enrollment
- Move-type auto-detection (renting-to-renting, first home purchase, sell-and-buy, work relocation, downsizing)
- Smart templates per move type with lead-time-aware checklists
- Built-in address change checklist (USPS, banks, insurance, subscriptions, employer, doctors, schools, etc.)
- Mover and vendor tracking with quotes and scheduling
- Utility transfer tracking (start/stop dates per service)
- Light financial tracking for moving expenses
- Persistent storage in `move-data.json`
