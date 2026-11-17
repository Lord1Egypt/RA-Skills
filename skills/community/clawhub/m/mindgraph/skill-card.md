## Description:

Create and query an Obsidian-style wikilink knowledge graph with learnable repeatable MindSkills for managing and analyzing workspace Markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hulkworks](https://clawhub.ai/user/hulkworks)

### License/Terms of Use:


## Use Case:

Developers and workspace agents use Mindgraph to index Markdown notes, query wikilink relationships, find disconnected knowledge, and run repeatable MindSkill processes that save structured Markdown results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence ordinary Markdown edits across a workspace and create persistent files.

Mitigation: Use it only in workspaces where Obsidian-style wikilinks are desired, and review generated Markdown and index updates before relying on them.

Risk: The security evidence identifies an unbounded path-handling flaw in MindSkill commands.

Mitigation: Avoid untrusted or path-like MindSkill names until path validation is added.

## Reference(s):

- [Mindgraph ClawHub skill page](https://clawhub.ai/hulkworks/skills/mindgraph)
- [MindGraph Philosophy](artifact/references/philosophy.md)
- [Knockout Test MindSkill Process](artifact/mindskills/knockout-test/PROCESS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated Markdown files; CLI commands also produce plain text and JSON index files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates workspace Markdown files, MindSkill result files, and a persistent mindgraph.json index.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
