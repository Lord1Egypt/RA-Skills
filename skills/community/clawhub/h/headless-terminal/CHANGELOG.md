# Changelog

## 1.0.0

Initial public release.

### Added
- Guidance for driving hostile or full-screen terminal UIs with Montana Flynn's `ht` CLI
- Wait/synchronization decision guidance for `--wait-text`, `--wait-idle`, `--wait-exit`, and related patterns
- References for examples, key notation, recipes, troubleshooting, and wait strategy
- Guidance for cleanup, unique session naming, and failure recovery

### Changed
- Prefer ordinary shell I/O, PTY shell control, or tmux when those fit better
- Treat `ht` as a specialized tool rather than the default answer for terminal work
- Name the expected install source explicitly: `montanaflynn/headless-terminal`

### Hardening
- Added false-friend warnings for unrelated `ht` packages
- Replaced local/private hostname examples with neutral placeholders
- Added trust guidance around taps, release artifacts, and package ambiguity
- Added stronger caution around privacy-sensitive, remote, or destructive TUI flows
