## Description:

Enforces Markdown output formatting policy when users request full Markdown source code, raw Markdown, or copyable Markdown documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeff-tian](https://clawhub.ai/user/jeff-tian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation authors use this skill to make agents return copyable Markdown source with consistent outer fencing and link-spacing rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can alter standard Markdown link syntax by adding spaces before closing parentheses and after bare URLs.

Mitigation: Review generated Markdown when standard Markdown parser compatibility is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeff-tian/skills/markdown-output)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown text wrapped in triple tilde fences when full Markdown source is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adds nonstandard spaces in Markdown links and after bare URLs according to the skill policy.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
