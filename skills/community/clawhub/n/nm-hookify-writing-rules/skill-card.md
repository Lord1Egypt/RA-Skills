## Description:

Writes hookify rules in markdown that block dangerous commands or restrict AI behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to write persistent hookify rules that warn about or block unwanted commands and behavior in Claude Code sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports partial scan coverage, and the examples include rules that can block commands and instructions to delete local rule files.

Mitigation: Review each rule's event, pattern or conditions, and action; test matching and safe non-matching inputs, and back up rule files before removing them.

## Reference(s):

- [Hookify plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/hookify)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown rule-file guidance with YAML frontmatter, regex patterns, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples include hookify rule files and optional commands for testing regex patterns.]

## Skill Version(s):

1.10.3 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
