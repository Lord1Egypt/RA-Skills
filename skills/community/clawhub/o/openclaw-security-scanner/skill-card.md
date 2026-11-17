## Description:

Runs a local security assessment for OpenClaw installations, checking configuration, network exposure, credential hygiene, OS hardening, and agent guardrails with optional reporting and fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkahn-tr](https://clawhub.ai/user/jkahn-tr)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to run local security scans of their own OpenClaw installation, review severity-ranked findings, and optionally generate text or JSON reports. The optional fix mode can suggest or apply selected local hardening changes after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional auto-fix mode uses shell evaluation that can run unintended commands in some setups.

Mitigation: Run the read-only scan first. Use --fix only after reviewing the script, with a trusted simple OPENCLAW_HOME path, and confirm only fixes you understand.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jkahn-tr/skills/openclaw-security-scanner)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance, Files]

**Output Format:** [Terminal text, optional JSON, and optional timestamped text or JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; --fix prompts before applying changes; --report writes a local report file.]

## Skill Version(s):

1.0.0 (source: server release metadata and script header)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
