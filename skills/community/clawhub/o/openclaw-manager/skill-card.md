## Description:

Deploy, harden, and operate OpenClaw across local and hosted environments (Fly.io, Render, Railway, Hetzner, GCP) with secure defaults, channel setup guidance, integration onboarding, and troubleshooting workflows grounded in official OpenClaw documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollaugo](https://clawhub.ai/user/hollaugo)

### License/Terms of Use:


## Use Case:

Developers, operators, and platform engineers use this skill to plan, validate, deploy, harden, and operate OpenClaw in local or hosted environments with documented security gates and operations ledger updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Environment validation output can expose sensitive .env contents when logs are retained.

Mitigation: Review the skill before production use, avoid running the validator where output is logged until malformed-line redaction is fixed, and keep validation logs out of shared systems that may capture secrets.

Risk: Operations ledger entries can become misleading if untrusted or unsanitized values are passed to the ledger updater.

Mitigation: Pass only trusted operational values, review ledger entries before handover, and store ledger records in a structured or sanitized format when they are used for audit decisions.

Risk: OpenClaw rollouts may involve provider secret writes, public network exposure, and persistent state changes.

Mitigation: Require profile validation, documented rollback ownership, mandatory security checklist pass, and ledger updates before go-live.

## Reference(s):

- [OpenClaw Doc Map](references/openclaw-doc-map.md)
- [OpenClaw Security Checklist](references/openclaw-security-checklist.md)
- [OpenClaw Mode Matrix](references/openclaw-mode-matrix.md)
- [OpenClaw OS Matrix](references/openclaw-os-matrix.md)
- [OpenClaw Integrations Playbook](references/openclaw-integrations-playbook.md)
- [OpenClaw Ops Ledger Schema](references/openclaw-ops-ledger-schema.md)
- [OpenClaw Getting Started](https://docs.openclaw.ai/start/getting-started)
- [OpenClaw Install Overview](https://docs.openclaw.ai/install)
- [OpenClaw Security Overview](https://docs.openclaw.ai/security)
- [OpenClaw Remote Access Hardening](https://docs.openclaw.ai/remote-access)
- [OpenClaw Open Source Repository](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON validation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce rollout plans, environment validation results, operations ledger entries, security gate summaries, channel and integration matrices, and risk-ordered follow-up actions.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
