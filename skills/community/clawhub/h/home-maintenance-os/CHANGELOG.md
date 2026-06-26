# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] — 2026-05-13

### Changed
- Frontmatter `version` field now quoted as a string per ClawHub CLI requirements
- Added this CHANGELOG.md for consistency with the rest of the published skill catalog

### Notes
- No behavior changes in this release. Purely documentation and metadata cleanup.

## [1.0.0] — 2026-04-12

### Added
- Initial release
- Living record for every appliance, system, contractor, and maintenance task in a home
- Appliance tracking (HVAC, water heater, washer, dryer, refrigerator, more) with install dates, warranties, and service history
- Contractor directory (plumber, electrician, HVAC, handyman, landscaper, etc.) with notes and pricing history
- Built-in maintenance knowledge with time-based and mileage-equivalent intervals
- Service history per appliance and per contractor
- Cost tracking with annual rollups and per-system spending summaries
- Multi-property support for homeowners managing more than one home
- Persistent storage in `home-data.json`
