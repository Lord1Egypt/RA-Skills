# ios-dev-cleanup

Scan and clean up iOS development disk usage — simulators, runtimes, DerivedData, CocoaPods cache, archives, and more. Works as a Claude Code or OpenClaw skill.

## Features

Scans **8 categories** of iOS development disk usage:

| # | Category | Typical Size |
|---|----------|-------------|
| 1 | Simulator Runtimes | 10-55 GB |
| 2 | Simulator Devices | 1-10 GB |
| 3 | CocoaPods Cache | 5-15 GB |
| 4 | iOS DeviceSupport | 3-10 GB |
| 5 | DerivedData | 2-20 GB |
| 6 | Archives | 0-10 GB |
| 7 | SPM Cache | 0-2 GB |
| 8 | Caches & Logs | varies |

Each category shows **top 5 items by size** with last-used timestamps. Unavailable simulators/runtimes are auto-cleaned before the scan.

## Quick Start

### Install

**Claude Code (recommended):**
```bash
cd ~/.claude/skills
git clone https://github.com/jesseluo/ios-dev-cleanup.git
```

**OpenClaw:**
```bash
clawhub install ios-dev-cleanup
# or manually:
cd ~/.openclaw/skills
git clone https://github.com/jesseluo/ios-dev-cleanup.git
```

**Project-level (single repo):**
```bash
cd your-project
git clone https://github.com/jesseluo/ios-dev-cleanup.git .claude/skills/ios-dev-cleanup
```

### Configure

No additional configuration needed. The skill uses standard macOS/Xcode CLI tools.

### Verify

In Claude Code, run:
```
/ios-dev-cleanup
```
You should see a disk usage scan across all 8 categories.

## Usage

**Trigger** the skill by asking Claude Code to check iOS disk usage or clean up development artifacts:

- `/ios-dev-cleanup`
- "Check my iOS disk usage"
- "Clean up simulators"
- "How much space is DerivedData using?"

**Workflow:**
1. **Scan** — all 8 categories are scanned, unavailable items auto-cleaned
2. **Review** — summary table + per-category Top 5 details presented
3. **Choose** — you select which categories to clean
4. **Clean** — deletion executed with before/after size comparison

## Security

- **Safe deletion commands**: Simulators and runtimes are deleted via `xcrun simctl` only, never `rm -rf`
- **User confirmation required**: No data is deleted without explicit user approval (except unavailable simulators/runtimes which are already non-functional)
- **No network access**: The skill only reads local filesystem and Xcode CLI output
- **No data exfiltration**: No data is sent anywhere; all operations are local

## Compatibility

- **OS**: macOS (tested on macOS 15+)
- **Xcode**: 16+ (compatible with earlier versions for most categories)
- **Runtime dependencies**: `xcrun`, `du`, `stat` (all included with macOS/Xcode)
- **Platforms**: Claude Code, OpenClaw

## License

MIT License — see [LICENSE](LICENSE) for details.
