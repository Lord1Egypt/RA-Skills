# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.0.0] - 2026-03-03

### Added
- ClawHub skill manifest (`clawhub.json`) for marketplace publishing
- Comprehensive `SKILL.md` for AI agent integration
- Screenshots directory for ClawHub listing
- Permission justification documentation

### Changed
- Updated README with troubleshooting section and permission documentation

## [4.0.0] - 2026-02-15

### Added
- Home access section (keys, codes, alarm, WiFi, parking)
- YAML config file support for business presets
- Example config files for boarding, walking, and in-home sitting
- `--no-home-access` flag to omit home access section

### Changed
- Reorganized form sections for better flow
- Improved authorization section with more comprehensive agreements

## [3.0.0] - 2026-01-20

### Added
- Service-specific templates: boarding, walking, drop-in
- Multi-pet support (1-10 pet profiles per form)
- `--service-type` and `--pets` CLI options

### Changed
- Form structure now adapts based on service type

## [2.0.0] - 2025-12-10

### Added
- 7 color themes: lavender, ocean, forest, rose, sunset, neutral, midnight
- `--theme` and `--list-themes` CLI options
- Custom color support via config file

### Changed
- Redesigned form layout with theme-aware styling

## [1.0.0] - 2025-11-01

### Added
- Initial release
- Fillable PDF form generation with ReportLab
- Pet owner information section
- Pet profile section
- Vaccinations with checkboxes
- Health and medications section
- Behavior and temperament section
- Feeding and daily care section
- Authorization and signature section
- Basic CLI with business name, contact, and output options
