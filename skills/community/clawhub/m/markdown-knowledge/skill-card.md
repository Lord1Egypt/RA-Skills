## Description:

Integrates a local Markdown knowledge base with OpenClaw so agents can search Markdown files and inject relevant snippets only when the user explicitly requests it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronjager92](https://clawhub.ai/user/aaronjager92)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to make a local Markdown notes directory searchable from OpenClaw conversations, rebuild the local index, and retrieve relevant snippets for context-aware answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published package includes private indexed data and credentials.

Mitigation: Remove the bundled index before installation, rotate any exposed credentials, and keep secrets out of Markdown notes that may be indexed.

Risk: Setup may download and install ripgrep without explicit consent or integrity verification.

Mitigation: Require explicit user approval for dependency installation and verify downloaded binaries, or install ripgrep through a trusted package manager.

Risk: Retrieved note content can be injected into conversations and exposed in generated answers.

Mitigation: Configure a narrow knowledge_path, use exclude_patterns for sensitive folders, and review retrieved snippets before sharing responses outside the intended context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaronjager92/skills/markdown-knowledge)
- [Publisher Profile](https://clawhub.ai/user/aaronjager92)
- [Project Reference](references/PROJECT.md)
- [README](references/README.md)
- [ripgrep 14.1.4 Release Downloads](https://github.com/BurntSushi/ripgrep/releases/download/14.1.4)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text responses with optional JSON-like search, build, and stats results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search behavior is controlled by local configuration such as knowledge_path, index_path, search_top_k, auto_refresh, and exclude_patterns.]

## Skill Version(s):

1.1.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
