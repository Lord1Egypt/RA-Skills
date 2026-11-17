## Description:

Uses OOMOL's oo CLI to read and manage LangSmith datasets, examples, projects, and workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to read and manage LangSmith datasets, examples, tracing projects, and workspaces through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified internet code without asking first, and may install or update additional agent skills.

Mitigation: Review and verify the CLI installer and any additional skills it installs or updates before authorizing setup.

Risk: LangSmith requests pass through OOMOL, while the remote installation and authentication implementations and credential storage are not verified in the release files.

Mitigation: Use an API key limited to the intended work and account for OOMOL handling requests when deciding what data to access.

## Reference(s):

- [LangSmith](https://www.langchain.com/langsmith)
- [LangSmith API reference](https://docs.langchain.com/langsmith/smith-api-ref)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-langsmith)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and shell commands with usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include execution metadata.]

## Skill Version(s):

1.0.4 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
