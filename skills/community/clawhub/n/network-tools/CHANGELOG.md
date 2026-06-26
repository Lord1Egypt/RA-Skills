# Network Tools Skill Changelog

## v2.0.0 (2026-04-07)

### Added
- **Comprehensive network diagnostics**: DNS, ping, traceroute, whois, IP info commands
- **Enhanced download capabilities**: Resume support, multiple output formats, smart filename generation
- **Media downloading**: youtube-dl integration for video/audio from 1000+ sites
- **Intelligent tool selection**: Auto-selects best tool based on content type and file size
- **User-agent rotation**: Anti-detection with realistic browser user agents
- **Multiple service fallback**: IP info uses multiple services for reliability
- **Detailed tool discovery**: `tools` command shows availability of all network utilities

### Improved
- **Error handling**: Better error messages and graceful degradation
- **Documentation**: Comprehensive SKILL.md with detailed usage examples
- **Security**: Enhanced input validation and URL sanitization
- **Proxy support**: Works with all tools through environment variables or native options
- **Performance**: Optimized options for each tool (timeouts, retries, compression)

### Fixed
- **Tool compatibility**: Proper handling of different tool capabilities
- **Filename safety**: Prevents directory traversal in output filenames
- **URL validation**: Ensures proper http/https URL format

### Removed
- **Overpromising features**: Previous documentation claimed features that weren't implemented
- **Incomplete implementations**: Replaced minimal script with fully functional version

## v1.0.0 (Initial)

- Basic fetch and download functionality
- Simple proxy support
- Minimal tool detection