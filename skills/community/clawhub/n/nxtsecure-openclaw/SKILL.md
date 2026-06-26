---
name: openclaw-security-audit
description: Use when auditing and remediating an OpenClaw Linux host with a nightly 23:00 security run. Covers firewall status, fail2ban bans, SSH hardening with key-only auth and a non-default port, unexpected listening ports, Docker container allowlisting, disk usage under 80%, failed login attempts in the last 24 hours, automatic security package updates, VirusTotal browser-based checks for URLs and files without API keys, and installing the cron entry.
homepage: https://openclaw.ai/
---

# OpenClaw Security Audit

Original requested prompt, preserved verbatim:
"Effectuez un audit de sécurité tous les soirs à 23h faite un cron."

Use this skill when the user wants a repeatable OpenClaw host security audit, a nightly cron job, or immediate remediation of common hardening gaps.

## Workflow

1. First install or verify the CLI so the agent uses a stable interface:
   `npm install -g nxtsecure-openclaw`
   then verify with:
   `nxtsecure openclaw doctor`
2. If the CLI cannot be installed globally, fall back to the repository copy in `{baseDir}/../../bin/nxtsecure.mjs`.
3. From the repository root, create the local configuration with `nxtsecure openclaw config init --output ./openclaw-security-audit.conf` or copy `{baseDir}/references/openclaw-security-audit.conf.example`.
4. Run `nxtsecure openclaw audit --config ./openclaw-security-audit.conf` to execute the audit and remediation workflow.
5. Install the nightly 23:00 cron entry with `nxtsecure openclaw cron install --log ~/openclaw-security-audit.log`.
6. If every check passes, print exactly `audit de sécurité réussi`.
7. If a check fails, explain the issue, attempt remediation immediately, and rerun the relevant verification.

## Checks

The audit must verify:

1. Firewall enabled.
2. `fail2ban` active and total banned IP count collected.
3. If SSH is used, password authentication must be disabled, public key authentication must be available, and the SSH service must not listen on port `22`.
4. Unexpected listening ports identified and, when configured, blocked.
5. Docker containers reviewed when Docker is present, with unexpected containers stopped only when an allowlist is configured.
6. Disk usage below `80%` on persistent filesystems.
7. Failed login attempts during the last 24 hours.
8. Automatic security package updates enabled on the host.
9. If VirusTotal is configured, URLs and files in scope must be checked before being trusted.

## SSH hardening guidance

When SSH is enabled, the agent must help the user migrate safely instead of changing access blindly.

1. Explain the goal: SSH on a non-default port and key-only authentication.
2. Ask or infer the target SSH port from configuration. Use `2222` only as a fallback example, not a forced default.
3. Help the user generate a key pair if needed:
   `ssh-keygen -t ed25519 -C "openclaw-admin"`
4. Help the user install the public key on the server:
   `ssh-copy-id -p <new-port> <user>@<host>`
   or append the public key to `~/.ssh/authorized_keys` with correct permissions.
5. Update SSH to use the chosen non-default port and disable password authentication.
6. Make sure the firewall allows the new SSH port before reloading SSH.
7. Tell the user to open a second terminal and verify:
   `ssh -p <new-port> <user>@<host>`
8. Only after the new key-based login works, remove any temporary legacy access and confirm the hardening is complete.

If the agent cannot verify that key-based access on the new port works, it must explain the exact manual steps still required and avoid risky lockout actions.

## VirusTotal guidance

When the user wants file or link reputation checks, the agent must use VirusTotal without an API key:

1. Use the OpenClaw `browser` tool, not the VirusTotal API.
2. Ensure the OpenClaw browser tool is enabled before starting the workflow.
3. For files, compute the SHA-256 locally first and prefer the public report page for an existing report.
4. Only upload a file through the VirusTotal website when the user has explicitly allowed it, because website uploads may disclose the sample outside the organization.
5. For URLs, open the public VirusTotal URL page in the browser tool and submit the URL for analysis through the web interface.
6. If a file or URL is malicious, explain the verdict. For files, ask the user whether to keep or remove the file. For URLs, recommend blocking the URL or domain.
7. If an item is suspicious, explain the risk and require explicit user confirmation before trusting it.
8. For nightly automation, treat VirusTotal as browser-assisted review.
9. If VirusTotal flags a file as malicious or suspicious, the agent must ask the user whether to keep or remove the file. The user always decides.
10. Do not claim that a URL or file was cleared automatically when the agent has only prepared the VirusTotal browser workflow and not inspected the result page.

Use the bundled helper:

- `nxtsecure openclaw vt url https://example.test`
- `nxtsecure openclaw vt file /path/to/sample.bin`
- fallback: `{baseDir}/scripts/openclaw_virustotal_check.sh --url https://example.test`
- fallback: `{baseDir}/scripts/openclaw_virustotal_check.sh --file /path/to/sample.bin`

OpenClaw browser flow:

1. `browser.start`
2. `browser.open` or `browser.navigate` to `https://www.virustotal.com/gui/home/url` for URLs
3. `browser.open` or `browser.navigate` to `https://www.virustotal.com/gui/home/upload` for files
4. Use `browser.snapshot` and `browser.act` to type, upload, and inspect detection results

## Operational notes

- Run the audit as `root` when possible. Some remediations require privileged access.
- Adjust expected ports and allowed Docker containers before enabling strict enforcement.
- The bundled script prefers `ufw`, then `firewalld`, then a non-empty `nftables` ruleset for firewall detection.
- The script uses `sshd -T` when available and falls back to SSH config files.
- The bundled SSH policy expects a non-default port whenever SSH is enabled. Port `22` is treated as non-compliant.
- The audit should enable automatic security updates when supported by the distribution, such as `unattended-upgrades` on Debian or Ubuntu and `dnf-automatic` on RPM-based hosts.
- Failed logins are collected from `journalctl`, `lastb`, or `/var/log/auth.log`, depending on what the host exposes.
- VirusTotal checks in this skill are intentionally API-free and rely on the public website plus the OpenClaw browser tool.
- The nightly cron line installed by the helper is `0 23 * * *`.

## Files

- `{baseDir}/../../package.json`: npm package definition for the `nxtsecure openclaw` CLI.
- `{baseDir}/../../bin/nxtsecure.mjs`: npm CLI entrypoint for audit, cron, VirusTotal, and config init.
- `{baseDir}/scripts/openclaw_security_audit.sh`: audit and remediation runner.
- `{baseDir}/scripts/openclaw_virustotal_check.sh`: VirusTotal URL and file reputation helper.
- `{baseDir}/scripts/install_cron.sh`: idempotent cron installer for `23:00` every day.
- `{baseDir}/references/openclaw-security-audit.conf.example`: baseline configuration template.
