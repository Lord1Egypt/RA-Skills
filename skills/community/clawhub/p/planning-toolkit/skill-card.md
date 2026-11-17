## Description:

Planning Toolkit helps agents write requirements, decompose work into reviewable tasks, maintain persistent planning files, run iterative execution loops, and clean up implementation work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to turn ambiguous work into reviewed specs, vertical task plans, persistent planning artifacts, iterative execution loops, and cleanup passes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The initialization script can write or delete files outside the intended planning folder if given a crafted task slug.

Mitigation: Use only simple lowercase slugs containing words, digits, and hyphens until slug validation and path traversal handling are fixed.

Risk: The skill creates persistent local planning files and may guide agents through iterative work or cleanup passes.

Mitigation: Review generated planning files and proposed cleanup changes before relying on them for project decisions or code changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/planning-toolkit)
- [Publisher profile](https://clawhub.ai/user/paudyyin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands, planning templates, and JSON loop state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create persistent local planning files and loop-state files when its scripts are used.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
