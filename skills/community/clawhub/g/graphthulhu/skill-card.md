## Description:

Knowledge graph MCP server for Logseq and Obsidian. 37 tools for reading, writing, searching, and analyzing your second brain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skridlevsky](https://clawhub.ai/user/skridlevsky)

### License/Terms of Use:


## Use Case:

External users and developers use graphthulhu to connect an agent to Logseq or Obsidian for reading, writing, searching, analyzing, and maintaining a knowledge graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an unpinned third-party executable with broad read, write, move, rename, delete, and bulk update access to Logseq or Obsidian content.

Mitigation: Install only from a trusted publisher, pin a reviewed version, verify release integrity when available, and require explicit approval before destructive or bulk update actions.

Risk: Misconfiguration or unintended tool use could alter or remove notes in a personal knowledge graph.

Mitigation: Back up the vault or graph before use and review proposed write, delete, move, rename, and property update operations before execution.

Risk: Logseq use requires a token that grants API access to the graph.

Mitigation: Store the Logseq token carefully, limit exposure to local trusted environments, and rotate it if it may have been exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/skridlevsky/skills/graphthulhu)
- [GitHub Repository](https://github.com/skridlevsky/graphthulhu)
- [GitHub Releases](https://github.com/skridlevsky/graphthulhu/releases)
- [Full Tool Reference](https://github.com/skridlevsky/graphthulhu#tools)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the graphthulhu binary; configured actions can read, write, move, rename, delete, and bulk update knowledge graph content.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
