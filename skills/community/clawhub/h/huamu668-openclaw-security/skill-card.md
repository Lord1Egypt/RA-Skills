## Description:

OpenClaw Security Guide provides security practices for root-enabled AI agents, covering command review, skill installation audits, permission tightening, hash baselines, business risk checks, nightly audits, and backup guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huamu668](https://clawhub.ai/user/huamu668)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to review and configure security practices for OpenClaw or Claude Code environments where agents may have elevated host access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review identified a recommendation for automatic daily Git backups that may include sensitive OpenClaw credentials, identity state, paired-device state, or secret-bearing configuration.

Mitigation: Exclude sensitive state from Git backups, or use client-side encrypted backups with separate key management, explicit user approval, minimal retention, secret scanning, and credential rotation procedures.

Risk: The artifact includes examples involving cron jobs, sudo, and chattr hardening steps that can change persistence or host protections.

Mitigation: Require explicit approval before installing cron jobs or running sudo or chattr hardening steps, and treat dangerous command examples as prohibitions unless separately approved.

## Reference(s):

- [OpenClaw Security Practice Guide](https://github.com/slowmist/openclaw-security-practice-guide)
- [SlowMist](https://www.slowmist.com/)
- [ClawHub Skill Page](https://clawhub.ai/huamu668/skills/huamu668-openclaw-security)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, tables, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for human review; it does not execute commands directly.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter guide version 2.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
