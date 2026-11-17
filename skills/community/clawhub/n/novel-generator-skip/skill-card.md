## Description:

Generates Chinese serialized web-novel prompts, outlines, chapters, continuity notes, and plot diagrams from a user's fiction direction or keywords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejianjun000](https://clawhub.ai/user/xiejianjun000)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creative-writing agents use this skill to turn a short Chinese fiction idea into a fuller prompt, outline, chapter files, continuity memory, and optional Mermaid-style plot diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow writes generated chapters, prompt files, diagrams, and continuity notes into local project directories.

Mitigation: Use the skill in a dedicated project directory and review output/ and .learnings/ before reusing or sharing the workspace.

Risk: The initialization script supports a --clean option that removes prior generated chapter files and resets story memory.

Mitigation: Run --clean only after confirming that existing output/ markdown files and .learnings/ notes no longer need to be preserved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejianjun000/skills/novel-generator-skip)
- [Prompt guide](artifact/references/prompt-guide.md)
- [Plot structures](artifact/references/plot-structures.md)
- [Examples](artifact/references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files and inline guidance, with optional Mermaid diagrams and shell commands for workspace initialization]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated novel prompts, outlines, chapters, diagrams, and continuity notes to local output/ and .learnings/ paths when used as directed.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill frontmatter, and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
