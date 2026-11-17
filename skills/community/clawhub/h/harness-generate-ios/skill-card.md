## Description:

Auto-generates a Claude Code harness for iOS and Swift projects, including CLAUDE.md, docs files, README quick-cards, and .claude/rules guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lidian6864677](https://clawhub.ai/user/lidian6864677)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to scan iOS and Swift projects and generate a compact Claude Code harness for project navigation, module documentation, coding rules, quality checks, and build guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan an entire iOS project and write or merge harness documentation and rule files.

Mitigation: Run it only in a workspace where generated changes can be reviewed, and inspect all generated or merged files before keeping them.

Risk: The skill includes post-generation memory-writing behavior that can affect future agent sessions without a clear opt-in.

Mitigation: Remove or disable the memory-writing section unless persistent harness-maintenance guidance is explicitly desired.

## Reference(s):

- [iOS Project Scan Procedures](references/scan-procedures.md)
- [Output File Templates](references/templates.md)
- [ClawHub skill page](https://clawhub.ai/lidian6864677/skills/harness-generate-ios)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files and inline shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or updates CLAUDE.md, docs files, README quick-cards, .claude/rules files, and an optional memory entry; generated files are marked for review.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
