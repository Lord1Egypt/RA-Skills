## Description:

Records and queries OpenClaw ecosystem deployments, including service registration, status updates, dependency checks, and port conflict checks, while avoiding credential values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain a local registry of OpenClaw deployments and services. It helps agents create service records, update service status, find existing services by port, type, or status, and document dependency and health-check details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist operational inventory such as ports, URLs, dependency names, and credential locations in memory/services/.

Mitigation: Use it only in workspaces where local deployment metadata may be retained, and record credential references without secret values.

## Reference(s):

- [OpenClaw deployment record specification](references/spec.md)
- [ClawHub skill listing](https://clawhub.ai/axelhu/skills/openclaw-deploy-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with service registry templates and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local files under memory/services/ when the agent applies the workflow.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
