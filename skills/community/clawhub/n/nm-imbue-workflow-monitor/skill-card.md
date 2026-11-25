## Description:

Detects workflow failures and inefficient patterns then files GitHub issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow maintainers use this skill to detect failures and inefficiencies, then prepare evidence-backed reports and file improvement issues on the configured Git platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command output or session details sent to GitHub or GitLab may contain sensitive information.

Mitigation: Review and remove sensitive details from content before sending it, and check the destination and content before issue creation or searches.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-imbue-workflow-monitor)
- [Related plugin page (listed in skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/imbue)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown reports and issue bodies, with shell examples and YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include reproducible command evidence, output excerpts, and session details.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
