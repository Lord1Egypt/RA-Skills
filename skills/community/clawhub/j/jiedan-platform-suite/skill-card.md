## Description:

Provides an installation entry point for nine third-party cinema ticketing platforms used with Cinema Agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rascalagnt001](https://clawhub.ai/user/rascalagnt001)

### License/Terms of Use:

MIT-0

## Use Case:

Cinema Agent operators and developers use this suite to install all nine ticketing-platform packages or select individual platforms for order synchronization and market analysis. Some listed platforms also declare pricing support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enabling external ticketing integrations may affect live order polling and pricing actions.

Mitigation: Before production use, verify Cinema Agent's polling frequency, platform credentials, pricing actions, and pause or removal controls.

## Reference(s):

- [Jiedan Platform Suite on ClawHub](https://clawhub.ai/rascalagnt001/skills/jiedan-platform-suite)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides suite-wide and per-platform installation guidance.]

## Skill Version(s):

1.2.7 (source: server-resolved release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
