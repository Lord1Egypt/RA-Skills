## Description:

Automated daily security audits for OpenClaw agents with DM delivery and optional email reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

AGPL-3.0-or-later

## Use Case:

Developers and security operators use this skill to schedule recurring OpenClaw security audits, summarize findings, and deliver reports to configured DM and optional email recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates or updates an unattended recurring OpenClaw audit job that sends reports to external DM and optional email recipients.

Mitigation: Review the cron payload, DM recipient, optional email recipient, SMTP settings, and install directory permissions before enabling the job.

Risk: Server security evidence flags report-integrity and transport risks for this release.

Mitigation: Prefer local sendmail or TLS-protected SMTP handling, keep git auto-pull disabled unless the release process is verified, and independently verify deep-audit results until the reported omission issue is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/openclaw-audit-watchdog)
- [ClawSec homepage](https://clawsec.prompt.security)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown reports with shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, openclaw, node, and configured DM delivery environment variables; optional email delivery uses sendmail or configured SMTP settings.]

## Skill Version(s):

0.1.6 (source: frontmatter, skill.json, changelog, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
