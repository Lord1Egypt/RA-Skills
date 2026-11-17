## Description:

Checks MCP servers against the PolicyLayer registry before an agent adds, installs, configures, or connects to them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[policylayer](https://clawhub.ai/user/policylayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run PolicyLayer prechecks or stack scans before adding MCP servers, then report registry verdicts and proposed deny rules to a human decision-maker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs remote npm package code from the live registry without a pinned version.

Mitigation: Install only if the publisher is trusted, and prefer a pinned package version before routine or persistent use.

Risk: The skill can install a persistent precheck hook or change agent settings.

Mitigation: Review hook and settings diffs, and require explicit human approval before persistent installation or configuration changes.

Risk: Registry lookup failures can leave a requested precheck incomplete.

Mitigation: Report the failed precheck clearly and do not substitute memory or an improvised scan as a verdict.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/policylayer/skills/mcp-precheck)
- [PolicyLayer skill source](https://policylayer.com/skill.md)
- [PolicyLayer dashboard](https://app.policylayer.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose MCP deny-rule configuration; persistent hook and settings changes require human approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
