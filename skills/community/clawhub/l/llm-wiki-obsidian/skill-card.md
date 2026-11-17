## Description:

Use when the user is working inside an Obsidian or markdown vault and wants to ingest sources, query accumulated knowledge, or maintain a Karpathy-style LLM wiki.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javastarboy](https://clawhub.ai/user/javastarboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge workers use this skill to have an agent co-maintain a persistent markdown or Obsidian wiki from curated source material, accumulated questions, and periodic maintenance passes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may read source material and create or revise generated wiki pages in a user's markdown or Obsidian vault.

Mitigation: Install this only for vaults where agent access is acceptable, and define raw-source and generated-wiki directories before use.

Risk: Batch ingest or lint passes may produce broad edits across the wiki.

Mitigation: Use version control or backups before larger maintenance passes so unwanted changes can be reviewed and reverted.

Risk: Sensitive notes, logs, or secrets stored in the vault may be included in agent-maintained wiki context.

Mitigation: Avoid storing secrets or sensitive logs in the vault unless a retention and access plan is in place.

## Reference(s):

- [qmd markdown search engine](https://github.com/tobi/qmd)
- [Tolkien Gateway example wiki](https://tolkiengateway.net/wiki/Main_Page)
- [ClawHub skill page](https://clawhub.ai/javastarboy/skills/llm-wiki-obsidian)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with proposed file edits, commands, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, revise, cross-link, and summarize markdown wiki pages based on user-provided sources and vault conventions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
