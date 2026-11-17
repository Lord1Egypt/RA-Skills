## Description:

Linear Agent lets agents manage Linear issues, workflows, cycles, projects, comments, backlog summaries, and commit-based issue updates through Linear's GraphQL API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdbotworker](https://clawhub.ai/user/clawdbotworker)

### License/Terms of Use:

MIT

## Use Case:

Developers and project teams use this skill to read, search, summarize, create, and update Linear workspace records from an agent or CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Linear personal API key and can access workspace data according to that key's permissions.

Mitigation: Use a limited or dedicated Linear token where possible and install the skill only in environments trusted to handle that token.

Risk: Create, update, move, post-comment, and sync-commit commands can make live Linear workspace changes without a dry-run or confirmation step.

Mitigation: Review commands and parameters before execution, and scope usage to trusted agent workflows for intended Linear workspaces.

## Reference(s):

- [ClawHub Linear Agent Skill Page](https://clawhub.ai/clawdbotworker/skills/linear-agent)
- [Linear API Settings](https://linear.app/settings/api)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Text]

**Output Format:** [Structured JSON responses with optional markdown summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may return counts, page information, summaries, Linear record data, or error messages.]

## Skill Version(s):

1.0.2 (source: CHANGELOG, package.json, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
