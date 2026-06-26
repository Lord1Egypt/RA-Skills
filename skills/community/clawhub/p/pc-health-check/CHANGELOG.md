# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2026-04-21

### Added
- `--save <path>` - Save report to file (cron-friendly, supports relative/absolute paths)
- `--silent` - Silent mode (save to file only, suppress terminal output)
- `--version` / `-v` - Print version number

### Fixed
- Report rendering: Device warnings and device errors now displayed as separate sections
- Report rendering: System events icon now reflects severity level

## [1.0.0] - 2026-04-19

### Added
- Initial release with 11 health check categories
- Quick mode (--quick) for 5 core checks in under 10 seconds
- Full mode for comprehensive 30-second system scan
- Automatic Markdown report generation
- Risk level classification (ok/warn/error) with visual indicators
- PowerShell UTF-8 encoding fix for Chinese character support
- Date parsing for PowerShell /Date(...)/ format
- Process name resolution for listening ports

### Features
- **OS Check**: Windows version, build, architecture, uptime
- **CPU Check**: Model, cores, threads, load percentage
- **Memory Check**: Total/used/free GB with usage percentage
- **Disk Check**: All logical drives with space usage
- **Network Check**: Active adapters, internet ping, DNS status
- **Process Check**: Top 10 by CPU and memory usage
- **Device Check**: Error/Unknown device detection
- **System Events**: Last 24h critical/error events
- **Startup Check**: Auto-start program list
- **Port Check**: Listening ports with high-risk detection (445, 3389, etc.)
- **Security Updates**: Recent Windows hotfixes

### Technical
- Zero external dependencies (pure Node.js)
- Cross-platform path handling
- JSON and Markdown output modes
- Robust error handling for each check

## Future Plans

- [ ] Temperature monitoring (CPU/GPU)
- [ ] Service status check
- [ ] Antivirus status detection
- [ ] Battery health (for laptops)
- [ ] Historical trend tracking
- [ ] Export to CSV/Excel
