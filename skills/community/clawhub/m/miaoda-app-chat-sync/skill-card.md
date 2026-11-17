## Description:

Convert Git repository code to structured JSON instructions for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoanso](https://clawhub.ai/user/xiaoanso)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to fetch Git repository contents and generate structured JSON instructions that another agent or automation system can review and apply for code synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private repository contents may be exported into JSON and passed to another agent.

Mitigation: Use trusted repository URLs and explicit commit hashes, exclude credential files such as .env files, and review the generated JSON before sharing or applying it.

Risk: Generated JSON can contain file overwrite instructions that a downstream agent may treat as authoritative.

Mitigation: Review generated file paths, file contents, and synchronization rules before execution; keep version control or backups available for rollback.

Risk: Private repository access may require a GitHub token.

Mitigation: Use a fine-grained read-only token scoped to the required repository and provide it only through the GITHUB_TOKEN environment variable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoanso/skills/miaoda-app-chat-sync)
- [README](artifact/README.md)
- [CHANGELOG](artifact/CHANGELOG.md)
- [Prompt configuration guide](artifact/PROMPTS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured JSON with optional Markdown-style terminal summaries and file output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository file contents, source metadata, file lists, change summaries, and agent-facing synchronization rules.]

## Skill Version(s):

3.2.1 (source: server release evidence and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
