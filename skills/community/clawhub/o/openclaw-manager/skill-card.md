## Description: <br>
Deploy, harden, and operate OpenClaw across local and hosted environments with secure defaults, channel setup guidance, integration onboarding, and troubleshooting workflows grounded in official OpenClaw documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollaugo](https://clawhub.ai/user/hollaugo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and platform teams use this skill to plan, validate, deploy or install, harden, and operate OpenClaw in local or hosted environments. It is especially suited for rollout planning, security gate checks, channel and integration setup, ops ledger updates, and incident-ready handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports administrative OpenClaw deployment operations, including provider secret writes, public network exposure, and persistent state changes. <br>
Mitigation: Run it only in an OpenClaw environment you control, use least-privilege credentials, and require explicit review before any secret write, deployment configuration change, or public exposure change. <br>
Risk: Weak, placeholder, duplicate, malformed, or missing environment values can lead to unsafe or failed deployments. <br>
Mitigation: Run the environment validation helper for the selected profile and block progression until required keys, provider alternatives, and gateway token strength checks pass. <br>
Risk: Public exposure without token controls, scoped ingress, TLS, or rollback ownership can create operational and security exposure. <br>
Mitigation: Complete the security checklist before go-live, document rollback ownership, and record required ledger events and blockers. <br>
Risk: Operations ledger entries may disclose operational metadata if written to an unintended path or populated with secret values. <br>
Mitigation: Confirm the ledger destination before writing, record key names and profile names only, and never record secret values. <br>


## Reference(s): <br>
- [OpenClaw Doc Map](references/openclaw-doc-map.md) <br>
- [OpenClaw Security Checklist](references/openclaw-security-checklist.md) <br>
- [OpenClaw Mode Matrix](references/openclaw-mode-matrix.md) <br>
- [OpenClaw OS Matrix](references/openclaw-os-matrix.md) <br>
- [OpenClaw Integrations Playbook](references/openclaw-integrations-playbook.md) <br>
- [OpenClaw Ops Ledger Schema](references/openclaw-ops-ledger-schema.md) <br>
- [OpenClaw Getting Started](https://docs.openclaw.ai/start/getting-started) <br>
- [OpenClaw Install Overview](https://docs.openclaw.ai/install) <br>
- [OpenClaw Security Overview](https://docs.openclaw.ai/security) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and optional JSON validation output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create rollout plan and operations ledger files when helper scripts are used.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
