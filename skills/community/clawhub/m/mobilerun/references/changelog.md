# Changelog

All notable changes to the Mobilerun skill are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- Troubleshooting guide with 10 common issues (references/troubleshooting.md)
- Searchable tags in SKILL.md frontmatter for ClawHub discovery
- Unicode/multi-language support documented for POST /keyboard
- Use case examples for non-developers (references/use-cases.md)
- Social proof: GitHub stars, TECNO EllaClaw OEM adoption, arXiv citation
- Active development links (PyPI, ClawHub listing)
- Resources section with community and documentation links
- Changelog

### Changed
- Restructured into references/ folder (setup-and-billing, troubleshooting, security, use-cases) for on-demand context loading
- Renamed "Before You Start" to "Quick Start"
- Rewrote intro paragraph with cloud device types (on-demand virtual, emulated, physical)

## [1.0.1] - 2026-02-10

### Changed
- Restructured as OpenClaw plugin monorepo
- Converted plugin to flat skill format

## [1.0.0] - 2026-02-08

### Added
- Initial release
- Device management API (list, provision, terminate cloud devices)
- Screen observation (screenshot, UI accessibility tree)
- Phone control (tap, swipe, type, press key, open/close apps)
- Tasks API for AI agent automation
- reference.md with auth setup, Portal APK guide, plans & billing, webhooks
- OpenClaw plugin metadata and CI packaging workflow
