# Changelog

## 2.0.0 - Persistent sessions and same-tab capture

- Replace process-name matching with private, locked per-session state and owned process-group cleanup; allocate and verify real loopback ports and Xauthority-protected displays.
- Capture an exact existing targetId without navigation; separate explicit navigation and URL-scoped cookie export. Preserve partial results with nonzero exit status.
- Add cooperative operator pause/resume and JSON start/status/pages/capture/stop commands.
- Read current-origin localStorage directly for existing CDP sessions; document omitted authentication state.
- Keep Chrome sandbox enabled and reject root Chrome. Remove executable .env loading, privileged auto-installs, global pkill and wget fallback.
- Add locked Playwright dependency, behavior tests, real CDP integration test and Linux lifecycle workflow.
- Breaking: named CLI arguments, explicit target/URL, new state/output layout, reduced supported config. See README migration.
- Withdraw unverified Docker instructions; Linux host deployment is the supported path.
- Retire incompatible legacy Docker files and systemd templates from the source repository.
- Align license and version metadata with the published MIT-0 skill card.

## 1.0.2 - Metadata & Documentation Fixes
- **Metadata:** Added explicit `required_env` YAML frontmatter to `SKILL.md` to properly communicate required variables to ClawHub registry parsers.
- **Documentation:** Extensively formatted `SKILL.md` (and `README.md`) using markdown code blocks and inline ticks to improve readability and distinctness of scripts, commands, and environment variables.


## 1.0.1 - Security & Configuration Hardening
- **Security:** Resolved Node script injection vulnerability in DevTools export scripts by using `process.argv` instead of unescaped interpolated string arrays.
- **Security:** Eliminated `VNC_PASSWORD` environment variable entirely to enforce secure `VNC_PASSFILE` usage. 
- **Setup:** Renamed `INSTALL.sh` to `setup.sh` to align with standard agent terminology.
- **Paths:** Replaced hardcoded `/tmp` paths and `SKILL_DIR=/` artifacts ensuring safer parameter-based execution and robust shebangs.
- **UX:** Added clear copyable `SSH tunnel` commands and local VNC loopback addresses to the `start_vnc.sh` standard output.
- **Metadata:** Disclosed explicit write and secret material access intents in `skill.json` and properly configured `required_env` bindings.
