## Description:

Defines security policies for agent workspaces, audits installed skills against those policies, checks command and network restrictions, and generates compliance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:

MIT

## Use Case:

Developers and workspace administrators use this skill to define local security policies, audit Agent Skills-compatible workspaces, check individual skills, and produce audit-ready compliance reports. It is most useful when a team needs repeatable workspace compliance checks before installing or running agent skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Under-documented enforcement and hook features can modify installed skills or affect future tool runs.

Mitigation: Use audit, check, report, and status for routine review; run enforce or protect only after manually reviewing the reported findings.

Risk: Generated Claude hook JSON may be unsafe when based on an untrusted or workspace-modifiable .marshal-policy.json.

Mitigation: Inspect generated hook JSON before adding it to settings and avoid generating hooks from untrusted policy files until shell-command construction is fixed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/atlaspa/skills/openclaw-marshal)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local JSON policy or hook configuration output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate on local workspace files; enforcement and protection commands can modify installed skills or generate hook JSON.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
