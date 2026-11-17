## Description:

Check for OpenClaw updates by comparing installed version against the npm registry and reporting status without modifying the system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfrederiksen](https://clawhub.ai/user/pfrederiksen)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check whether a globally installed OpenClaw package is current, including periodic update monitoring in cron or dashboard workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads known global OpenClaw package.json locations to determine the installed version.

Mitigation: Install only where read-only access to those package metadata paths is acceptable.

Risk: The skill sends a read-only HTTPS request to the public npm registry for OpenClaw version metadata.

Mitigation: Use it only in environments where outbound HTTPS access to registry.npmjs.org is approved.

## Reference(s):

- [OpenClaw npm registry metadata](https://registry.npmjs.org/openclaw)
- [OpenClaw release notes](https://github.com/openclaw/openclaw/releases/tag/v2026.2.21)
- [OpenClaw Update Checker on ClawHub](https://clawhub.ai/pfrederiksen/skills/openclaw-update-checker)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON status report, with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports installed version, latest version, update status, newer versions, and a changelog URL when available.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
