## Description:

NotebookLM Distiller: Batch knowledge extraction from Google NotebookLM into Obsidian. Supports Q&A generation (15-20 deep questions), structured summaries, glossary extraction, web research sessions, and direct markdown persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anchor-jevons](https://clawhub.ai/user/anchor-jevons)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-work agents use this skill to extract source-grounded NotebookLM content into Obsidian notes, create research notebooks, generate quiz questions, evaluate answers, and persist Markdown into a vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write durable Markdown files using user-supplied paths, and the security summary notes that write scoping is under-scoped.

Mitigation: Use a dedicated test vault or tightly controlled vault path, inspect destination paths before execution, and review generated files before merging them into a primary Obsidian vault.

Risk: The writeback option can add distilled content back into NotebookLM, creating durable changes outside the local vault.

Mitigation: Avoid autonomous writeback use; require explicit operator approval before adding sources back to NotebookLM.

Risk: The skill depends on the external notebooklm-py package and the NotebookLM CLI.

Mitigation: Pin notebooklm-py to a reviewed version and verify the installed CLI before use.

## Reference(s):

- [NotebookLM Distiller on ClawHub](https://clawhub.ai/anchor-jevons/skills/notebooklm-distiller)
- [Publisher profile: anchor-jevons](https://clawhub.ai/user/anchor-jevons)
- [OpenClaw](https://github.com/openclaw)
- [OpenClaw DeepReader](https://github.com/astonysh/OpenClaw-DeepReeder)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown notes with YAML frontmatter, JSON quiz or evaluation payloads, and command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write files under a user-supplied vault path and can optionally write distilled notes back into NotebookLM.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
