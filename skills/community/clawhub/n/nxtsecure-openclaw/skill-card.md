## Description:

Use when auditing and remediating an OpenClaw Linux host with a nightly 23:00 security run, covering firewall status, fail2ban bans, SSH hardening, listening ports, Docker allowlisting, disk usage, failed login attempts, automatic security package updates, VirusTotal browser-based checks, and cron installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scorpion7slayer](https://clawhub.ai/user/scorpion7slayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit and remediate OpenClaw Linux hosts and to schedule repeatable nightly security checks at 23:00.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged remediation may alter firewall, SSH, package update, Docker, or disk cleanup behavior on the host.

Mitigation: Review the configuration and run in audit-only mode first; avoid root execution until the scripts and settings are trusted.

Risk: SSH hardening can lock users out if key-based access on the new port is not confirmed before disabling legacy access.

Mitigation: Confirm key-based SSH login from a second session before allowing SSH changes or removing temporary access.

Risk: The nightly cron entry creates persistent scheduled execution and log output.

Mitigation: Inspect the cron line and log path before enabling the 23:00 nightly run.

Risk: Browser-based VirusTotal file review may disclose uploaded samples outside the organization.

Mitigation: Use existing public reports first and upload files only after explicit user approval.

Risk: Installing the npm CLI globally may pull an unexpected version.

Mitigation: Pin and verify the npm CLI version before installation or execution.

## Reference(s):

- [OpenClaw homepage](https://openclaw.ai/)
- [NxtSecure-openclaw ClawHub page](https://clawhub.ai/scorpion7slayer/skills/nxtsecure-openclaw)
- [VirusTotal URL review](https://www.virustotal.com/gui/home/url)
- [VirusTotal file review](https://www.virustotal.com/gui/home/upload)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include host audit findings, remediation steps, cron setup guidance, and VirusTotal browser review instructions.]

## Skill Version(s):

0.1.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
