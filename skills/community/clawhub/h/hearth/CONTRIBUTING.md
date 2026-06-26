# Contributing to hearth

Thanks for considering a contribution. hearth is a small project with a clear scope, so a few notes up front will save us both time.

## Scope

hearth is a **read-only health-check skill for homelab admins**. It is intentionally NOT:

- A monitoring system (use Prometheus/Grafana)
- An alerting system (use Alertmanager / Healthchecks.io)
- An automation system (use Ansible / Salt)
- A configuration management tool

Issues / PRs that move hearth toward any of those are likely to be politely declined. Issues / PRs that improve the core read-only sweep, add new device archetypes, fix bugs, or improve docs are very welcome.

## Before opening an issue

1. Check the [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) — most issues are documented there
2. Check existing issues — your problem might already be tracked
3. Include in your issue:
   - What platform you're running hearth on (Linux distro / macOS version / WSL version / Termux version)
   - What platform the device you're probing is
   - Sanitised excerpt of your `devices.yaml` (REDACT real IPs, hostnames, and tokens before pasting)
   - The exact output you got
   - The output you expected

## Before opening a PR

1. **Privacy first** — never include real IPs, real hostnames, real tokens, or real domain names in code, examples, or commit messages. Use the `192.0.2.0/24` documentation block (RFC 5737) and `example.com` for any sample data.
2. **Read-only invariant** — every probe must be read-only. No `systemctl restart`, no `apt-get install`, no `rm`, no writes to remote hosts beyond `/tmp/.hearth_*` files which are immediately cleaned up.
3. **Honest reporting** — if a layer cannot be probed for a given device type, the output must say so (e.g. "no-systemd (chroot — N/A)"), never silently fake a green result.
4. **Test it** — show that your change works against at least one real device before opening the PR.
5. **Document it** — if you add a new feature or device archetype, update the docs.

## Adding a new device archetype

If your homelab has a device type not covered by the existing six archetypes, a new archetype is a great contribution. The pattern:

1. Pick a generic name — `freebsd-host`, `truenas-server`, `proxmox-node` etc.
2. Add `examples/archetypes/<name>.md` describing the archetype and its probe specifics
3. Add a snippet to `examples/devices.example.yaml` showing the YAML for this archetype
4. Update the README archetype list

## Code style

- **Bash** — POSIX-leaning where possible, `bash` features OK if behind `#!/bin/bash`. Use `shellcheck` before submitting.
- **YAML** — 2-space indent, no tabs.
- **Markdown** — wrap at ~100 chars where natural, ATX headings (`#`, `##`, `###`).
- **Commit messages** — imperative mood, ≤72 char subject. Body wrapped at 72.

## License

By contributing, you agree your contributions will be licensed under the MIT License of this project.