## Description:

Command-line reference for listing, inspecting, and checking Moltbot skill availability and eligibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mondilo1](https://clawhub.ai/user/mondilo1)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to have agents inspect available Moltbot skills, view skill details, and troubleshoot missing binaries, environment variables, or configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may propose running local moltbot skills commands while inspecting skill availability.

Mitigation: Review command text before execution and keep usage to the documented read-oriented list, info, and check commands.

Risk: A skill may appear unavailable because required binaries, environment variables, or configuration are missing.

Mitigation: Use the documented eligibility and check commands to identify missing requirements before relying on the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mondilo1/skills/mondilo)
- [Skills system](/tools/skills)
- [Skills config](/tools/skills-config)
- [ClawdHub installs](/tools/clawdhub)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Markdown]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented CLI reference for moltbot skills list, info, and check commands.]

## Skill Version(s):

1.0.0 (source: server release evidence, created 2026-01-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
