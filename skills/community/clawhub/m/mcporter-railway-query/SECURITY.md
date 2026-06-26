# Security Policy

## Supported Versions

This project contains no background services or runtime daemons.
It only provides OpenClaw skill scripts.

## Reporting a Vulnerability

If you discover a security issue, please open an issue.

## Security Design

- No dynamic code execution
- No shell injection
- No remote code download
- No hidden processes
- No data persistence
- All external commands (`mcporter`) are invoked with fixed, user-controlled parameters only

### Behavior Transparency

The helper scripts in `scripts/` invoke the `mcporter` CLI tool as a subprocess. This is the sole external dependency and is always called with predictable, user-supplied arguments (date, station codes, filter flags). No other external commands, network requests, or runtime dependencies exist in this project.

This project acts as a thin wrapper around 12306 MCP interface via `mcporter`.
