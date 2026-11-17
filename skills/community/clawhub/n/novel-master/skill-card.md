## Description:

Publication-grade Chinese long-form novel writing kit that helps agents plan worlds, characters, outlines, chapters, foreshadowing, and quality control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bbroot](https://clawhub.ai/user/bbroot)

### License/Terms of Use:

MIT

## Use Case:

External writers, creators, and agent operators use this skill to structure and draft Chinese novels from initial concept through long-form continuity management and chapter quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts can read or write outside the intended novel workspace when given crafted project names.

Mitigation: Use only trusted novel project names and avoid slashes, backslashes, dots, or absolute paths until path validation and containment checks are added.

Risk: The skill maintains persistent manuscript state under ~/.qclaw/workspace/novels/.

Mitigation: Review expected file changes before running helper scripts and keep project-specific backups for long-running manuscripts.

## Reference(s):

- [README](README.md)
- [English README](README_EN.md)
- [Banned Words](references/banned-words.md)
- [Character Design](references/character-design.md)
- [Classic Writing Books](references/classic-writing-books.md)
- [Cognitive Bias](references/cognitive-bias.md)
- [Dramaturgy](references/dramaturgy.md)
- [Foreshadowing](references/foreshadowing.md)
- [Genres](references/genres.md)
- [Node-Compressed Graph](references/node-compressed-graph.md)
- [Plot Structure](references/plot-structure.md)
- [Process per Character](references/process-per-character.md)
- [Quantum Auditor](references/quantum-auditor.md)
- [Scene Writing](references/scene-writing.md)
- [Style Guide](references/style-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with code blocks, JSON state snippets, and Python helper commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts may create and maintain persistent manuscript state under ~/.qclaw/workspace/novels/.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
