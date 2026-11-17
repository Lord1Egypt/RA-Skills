## Description:

Boost developer productivity with Gitai: An AI-powered Git automation tool that analyzes code changes and generates semantic Conventional Commits instantly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leandrosilvaferreira](https://clawhub.ai/user/leandrosilvaferreira)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to inspect repository changes, generate Conventional Commits-style messages, and run the Gitai CLI to commit selected changes. It can optionally push committed changes when the user explicitly requests that workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can commit and push repository changes through Gitai.

Mitigation: Review staged changes and generated commit messages before running Gitai, and use --push only when publication to the configured remote is intended.

Risk: Repository diffs may be sent to external AI providers configured in Gitai.

Mitigation: Do not use the skill on repositories containing secrets or sensitive proprietary code unless that use is approved.

Risk: The Gitai CLI and API-key configuration are external dependencies.

Mitigation: Install the CLI only from a trusted and pinned source, verify the local configuration, and protect or rotate API keys stored in ~/.gitai.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leandrosilvaferreira/skills/gitai-skill)
- [Publisher profile](https://clawhub.ai/user/leandrosilvaferreira)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent to check prerequisite CLI installation and configuration before running Gitai.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact files report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
