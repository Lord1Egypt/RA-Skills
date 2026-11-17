## Description:

Use this skill when you need to operate Dietu through its official CLI for A-share market queries, strategy screening, decision workflows, or agent automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenee](https://clawhub.ai/user/kenee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to authenticate to Dietu, choose stable CLI commands, and return structured A-share market, strategy, decision, trading, or review output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the CLI with an unpinned latest version can pick up unexpected package changes.

Mitigation: Prefer a reviewed pinned Dietu CLI version when available before using the skill in sensitive workflows.

Risk: Command-line credentials and local profile tokens can expose Dietu account access on shared or compromised machines.

Mitigation: Use least-privileged revocable PATs through environment variables for automation, avoid putting real passwords directly on the command line, and logout or rotate tokens after exposure.

## Reference(s):

- [Dietu CLI Agent Skill Page](https://clawhub.ai/kenee/skills/mibatt-dietu-cli-agent)
- [Authentication Reference](artifact/references/auth.md)
- [Command Reference](artifact/references/commands.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON, Markdown, table, or NDJSON CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers JSON for agent parsing, Markdown for user-facing summaries, table output for terminal inspection, and NDJSON for streaming-style lists.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
