## Description:

Runs a lightweight operational and security posture check for an OpenClaw deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a quick OpenClaw deployment health check, review runtime and exposure findings, and decide what to fix before production or wider rollout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Healthcheck output may include local status, listener, and recent log evidence from the audited machine.

Mitigation: Review the JSON output before sharing it outside the machine or team responsible for the audit.

Risk: A passing lightweight check does not prove an OpenClaw deployment is secure.

Mitigation: Use the result as an operator triage signal and perform separate host, network, and exposure review for internet-facing systems.

Risk: The skill runs local diagnostic commands and reads OpenClaw config and log locations.

Mitigation: Run it only on the intended host or workspace with operator approval.

## Reference(s):

- [OpenClaw Healthcheck Checklist](artifact/references/checklist.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [JSON healthcheck report with score, verdict, findings, recommendations, and evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output may include local status, listener, and recent log snippets; review before sharing outside the audited machine.]

## Skill Version(s):

0.1.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
