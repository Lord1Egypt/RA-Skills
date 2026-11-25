## Description:

Writes hookify rules in markdown that block dangerous commands or restrict AI behavior

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Code or OpenClaw use this skill to write persistent hookify rules in Markdown that warn about or block command and file patterns, helping define behavioral guardrails for agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial because some referenced local paths were missing, leaving related evidence incomplete.

Mitigation: Review the skill and its rules before installation, and test each rule against a matching input and a known-safe example.

## Reference(s):

- [Hookify project page](https://github.com/athola/claude-night-market/tree/master/plugins/hookify)

## Skill Output:

**Output Type(s):** [Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown rule files with YAML frontmatter, pattern examples, and explanatory messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rules can define events, regex patterns or conditions, and warn or block actions.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
