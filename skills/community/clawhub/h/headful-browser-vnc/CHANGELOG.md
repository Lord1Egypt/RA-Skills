# Changelog

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
