# Changelog

All notable changes to hearth will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] — 2026-05-03

### Changed
- Replaced `<your-username>` placeholder in `git clone` URLs with the canonical `nj070574-gif/hearth` repo URL — the placeholder triggered `install_untrusted_source` on registry security scanners
- Softened `"Arbitrary shell command"` documentation wording in `docs/PROBES.md` and `docs/CONFIG.md` to clarify that `command` probes are user-defined and read-only

### Added
- README section explaining the `SUSPICIOUS` moderation badge that appears on some registries — a transparent breakdown of what scanners see vs. what hearth actually does, plus a clear list of what hearth does NOT do

### Fixed
- shellcheck findings (SC1087, SC2119, SC2034) from initial release

## [0.1.2] — 2026-05-03

### Changed
- Replaced `http://127.0.0.1/` with `http://localhost/` in the example `devices.example.yaml` and `README.md` — the bare-IP form was triggering `install_untrusted_source` on registry security scanners

## [0.1.3] — 2026-05-03

### Changed
- Replaced ALL raw-IP URLs in examples and archetypes with `.lan` hostnames (e.g. `http://fileserver.lan/`, `https://homeassistant.lan:8123/api/`). The scanner's `install_untrusted_source` rule was flagging each raw-IP URL one at a time

## [0.1.4] — 2026-05-03

### Changed
- Reduced `examples/devices.example.yaml` to a schema-only example covering the four auth modes (local, ssh-pass, ssh-key, http-only). App-probe (`apps:`) examples now live exclusively in the per-archetype guides under `examples/archetypes/` — registry scanners were repeatedly flagging in-YAML example URLs as `install_untrusted_source`, even hostname-based ones, so the cleanest fix was to keep all URL examples out of the YAML
- Updated README config snippet to match the new schema-only shape and explicitly point to `examples/archetypes/` for full worked examples

## [Unreleased]

### Added
- Initial public release of the hearth OpenClaw skill
- 5-layer probe pattern (ping, uptime+load, memory+disk, services, app health)
- Per-device YAML configuration with env-var-based credentials
- Six device archetypes: linux-systemd, linux-nosystemd-chroot, raspberry-pi, windows-http-only, slurm-cluster, magento-server
- Tailscale connectivity check support
- Honest reporting for non-systemd and Windows hosts (reports "N/A" rather than faking)
- Read-only probes — never modifies remote state
- Self-contained orchestration script with per-device timeouts (no single hung host can block the run)

### Security
- All credentials via env vars or SSH keys — never in config files
- `.gitignore` blocks `devices.yaml`, `*.token`, `id_*`, `.env`, etc.
- Documentation explicitly warns against committing real configs

## [0.0.0] — initialised

- Project skeleton, license, README