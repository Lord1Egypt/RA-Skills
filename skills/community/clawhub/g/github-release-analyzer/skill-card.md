## Description:

Analyze GitHub repository releases and summarize release notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stoner-byte](https://clawhub.ai/user/stoner-byte)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to summarize the latest or recent formal GitHub releases for a repository, either on demand or through cron-style incremental monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cron state keys can escape the intended state directory and read or overwrite other JSON files the agent can access.

Mitigation: Avoid custom --state-key values until path validation is added, and review cron jobs or shared instructions that can set state keys.

Risk: GitHub release bodies are external content that may contain untrusted instructions.

Mitigation: Treat release bodies only as source material for summaries, and do not let release text control agent behavior.

Risk: Release monitoring depends on repository targets supplied by users or scheduled jobs.

Mitigation: Use trusted GitHub repository targets and review configured cron inputs before enabling recurring execution.

## Reference(s):

- [Execution Modes](references/execution-modes.md)
- [Summary Contract](references/summary-contract.md)
- [State Format](references/state-format.md)
- [Output Templates](references/templates.md)
- [ClawHub skill page](https://clawhub.ai/stoner-byte/skills/github-release-analyzer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown messages with JSON render payloads and shell commands for prepare, render, and cron state commit steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cron mode emits NO_REPLY when no formal release is selected; requires python3 and a GitHub repository input.]

## Skill Version(s):

0.0.5 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
