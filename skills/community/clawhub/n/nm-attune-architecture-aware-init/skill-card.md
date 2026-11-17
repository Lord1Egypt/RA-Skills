## Description:

Selects architecture paradigm via research before scaffolding

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers starting a project with an undecided architecture use this skill to research current practices, choose and justify an architecture, customize a project scaffold, and record the decision in an ADR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review noted a mismatch between the skill’s research-led purpose and a supplied command that applies a predetermined architecture; coverage is partial because two referenced paths were missing.

Mitigation: Check that the skill is being used for architecture initialization, confirm the selected architecture and rationale against project context and completed research, and verify that referenced materials are available before relying on affected workflow steps.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-attune-architecture-aware-init)
- [Attune plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Files, Configuration instructions, Shell commands]

**Output Format:** [Architecture recommendation and rationale, Markdown synthesis and ADR, scaffold files, and configuration or command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scaffold and ADR are created in the target project.]

## Skill Version(s):

1.10.3 (source: skill frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
