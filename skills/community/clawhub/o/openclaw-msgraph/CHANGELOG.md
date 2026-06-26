# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-03-03

### Added

- Initial release: Microsoft Graph Skill for OpenClaw
- Email management: inbox listing, read, move, folder browsing, search
- Calendar management: list events, get details, create events, list calendars
- PKCE OAuth authentication with local token storage
- Comprehensive test suite: 114 tests with 82% code coverage
- Full documentation: setup guide, skill guide, API reference
- Python 3.7+ compatibility with no external dependencies

### Features

- ✅ Secure PKCE authentication (no client secret required)
- ✅ Automatic token refresh on expiration
- ✅ Well-known folder shortcuts (inbox, drafts, sentitems, etc.)
- ✅ Custom folder name resolution by display name
- ✅ Rich datetime formatting with timezone support
- ✅ HTML content stripping for readable email display
- ✅ Event creation with attendees and location
- ✅ Calendar timezone support

### Code Quality

- Type hints throughout core modules
- Comprehensive docstrings
- Modular architecture (graph_api.py, utils.py shared modules)
- No code duplication (60+ lines consolidated)
- Full test coverage for HTTP utilities and formatters

### Documentation

- README with quick start guide
- Detailed setup instructions for Azure Portal config
- Skill guide with command reference and workflows
- Troubleshooting section
- API reference for Microsoft Graph endpoints

---

## Format

The rest of this file follows the [keepachangelog.com](https://keepachangelog.com) format:

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for in case of vulnerabilities
