## Description:

Generates Chinese long-form web novels from a short direction by expanding prompts, planning outlines, drafting chapters, maintaining continuity notes, and producing Markdown chapters and Mermaid diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ityhg](https://clawhub.ai/user/ityhg)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and creative-writing agents use this skill to turn a short Chinese fiction premise into a structured novel workflow with outlines, chapters, continuity records, and plot diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes generated chapters and continuity notes to local Markdown files.

Mitigation: Run it in the intended project workspace and avoid including sensitive story material unless local storage is acceptable.

Risk: The initialization script's --clean option deletes prior generated Markdown output and resets story memory files.

Mitigation: Use --clean only when starting over or after backing up any output and .learnings content that should be preserved.

## Reference(s):

- [Prompt Guide](references/prompt-guide.md)
- [Plot Structures](references/plot-structures.md)
- [Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)
- [self-improving-agent](https://github.com/peterskoett/self-improving-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files with prose chapters, outlines, continuity notes, Mermaid diagrams, and optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local output/ Markdown files and updates .learnings/ continuity notes; --clean resets prior output and memory files.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
