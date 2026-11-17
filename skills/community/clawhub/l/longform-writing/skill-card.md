## Description:

Guides agents through writing or continuing long documents with longform-memory MCP recall, open-thread tracking, chapter memory updates, and continuity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emberspun-ai](https://clawhub.ai/user/emberspun-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and agents use this skill to keep novels, manuals, courses, screenplays, and other chaptered projects consistent across context windows. It tells the agent when to recall context, draft, record chapter changes, and check continuity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses npx -y with an unpinned MCP package, which can install and run a package version that was not reviewed with this release.

Mitigation: Pin and verify the longform-memory-mcp package version before use, and avoid automatic npx installation where possible.

Risk: Manuscript text is stored as plaintext local files under ~/.longform-memory/.

Mitigation: Use this skill only with writing projects that are acceptable to store as local plaintext, and apply local access controls appropriate for the manuscript.

Risk: Continuity findings can be context-sensitive, such as dialogue from a dead character appearing in a flashback or memory.

Mitigation: Review quoted continuity evidence before making edits, especially for findings that are marked likely rather than certain.

## Reference(s):

- [Longform Memory documentation](https://emberspun.com/open-source/longform-memory)
- [Emberspun AI Book Writer](https://emberspun.com)
- [ClawHub skill listing](https://clawhub.ai/emberspun-ai/skills/longform-writing)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with JSON configuration and inline tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assumes access to the longform-memory MCP server and a consistent project name for the writing project.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
