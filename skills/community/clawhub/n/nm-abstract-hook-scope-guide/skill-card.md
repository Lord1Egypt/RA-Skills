## Description:

Select hook scope (plugin, project, global) by audience

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this guide to choose plugin, project, or global scope for Claude Code hooks based on audience, version-control needs, and desired persistence. It also identifies the configuration location for the selected scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global hooks can apply across all Claude sessions on the machine.

Mitigation: Before choosing global scope, check that this machine-wide reach matches the intended audience and persistence needs.

## Reference(s):

- [Claude Code Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [Claude Code Settings Configuration](https://docs.anthropic.com/en/docs/claude-code/settings)
- [Claude Night Market Abstract Plugin](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A scope recommendation with rationale and the corresponding configuration location.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
