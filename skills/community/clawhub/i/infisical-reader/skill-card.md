## Description:

Infisical Reader helps an agent fetch Infisical secrets directly through the REST API using a local machine identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[achikochikorogaru](https://clawhub.ai/user/achikochikorogaru)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when an agent needs to list Infisical projects or retrieve secrets for a specific workspace, environment, path, or key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose Infisical secret values to the agent session or downstream logs, especially when raw or JSON output is requested.

Mitigation: Use tightly scoped machine identities and avoid raw or JSON output unless the workflow requires it.

Risk: A broad Infisical machine identity could give the agent access to more projects, environments, or paths than needed.

Mitigation: Restrict the machine identity to the minimum required projects, environments, and paths.

Risk: The local Infisical client secret can grant access if it is copied, logged, or stored insecurely.

Mitigation: Store the client secret carefully and rotate it if exposure is suspected.

## Reference(s):

- [Infisical](https://infisical.com)
- [Infisical API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/achikochikorogaru/skills/infisical-reader)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Plain text or JSON, with Markdown documentation and inline bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Secret values are masked by default unless raw output is requested.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
