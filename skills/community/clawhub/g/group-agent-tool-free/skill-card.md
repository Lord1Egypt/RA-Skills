## Description:

A Chinese-language skill that guides agents through local group-agent CLI workflows for lightweight multi-agent group creation, mentions, broadcasts, member management, and message lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, independent builders, enterprise automation teams, and agent operators use this skill to coordinate small multi-agent project groups with command examples for group creation, invitations, announcements, mentions, channels, and archived message searches. The source explicitly excludes personnel performance evaluation, financial budget approval, and legal contract review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes broad file, API, and command automation language beyond the documented group-agent coordination workflow.

Mitigation: Keep execution scoped to the documented group-agent CLI commands and require explicit user approval before using unrelated shell automation.

Risk: The skill stores group data and logs locally through SQLite-backed examples.

Mitigation: Review configured database and log paths before use, and avoid placing secrets or sensitive operational data in group messages.

Risk: The skill allows shell-command-oriented workflows through the agent environment.

Mitigation: Review commands before execution, avoid command construction from untrusted input, and use allowlisted group-agent commands where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/group-agent-tool-free)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, YAML examples, JSON examples, and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local CLI command patterns for group-agent workflows and operational guidance for SQLite-backed single-instance usage.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
