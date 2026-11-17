## Description:

Memory Profiler: mines hidden patterns from an agent user's memory, confirms findings through an interactive quiz, and generates a structured user profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fret774](https://clawhub.ai/user/fret774)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use MemWeaver to analyze local OpenClaw memory files, validate inferred preferences and behavioral patterns through a questionnaire, and produce a structured YAML profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill analyzes private memory logs and may infer sensitive personal traits.

Mitigation: Run it only on memories the user intentionally wants analyzed, and review the .codebuddy files before collection.

Risk: Memory files may contain secrets or untrusted pasted instructions.

Mitigation: Remove secrets and suspicious content before analysis, and treat memory-derived findings as user-reviewed drafts.

Risk: Generated profiles and backups can expose sensitive personal data.

Mitigation: Store output profiles carefully and delete generated profile files and backups when they are no longer needed.

Risk: Custom input or output paths broaden local file access.

Mitigation: Use default paths when possible, and use custom --profile, --workspace, or --output paths only when the target path is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fret774/skills/memweaver)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [Profile dimensions](artifact/config/dimensions.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands, JSON memory collection output, and YAML profile files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local memory files and writes dated profile YAML files with backup behavior.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
