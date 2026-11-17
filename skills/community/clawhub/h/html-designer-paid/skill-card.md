## Description:

HTML设计工具 helps agents produce and refine HTML/CSS page design code, visual layout guidance, and UI/UX design recommendations for web design workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agents use this skill to generate HTML/CSS layout code and design-review guidance for web pages, visual optimization, responsive layout work, and UI/UX iteration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad command execution and file mutation authority that is not tightly scoped to its HTML/CSS design purpose.

Mitigation: Install only in a supervised or sandboxed agent environment, review proposed commands before execution, and restrict write access to intended project files.

Risk: The artifact describes API key configuration and command-based troubleshooting, which can expose credentials or sensitive files if used carelessly.

Mitigation: Store credentials in environment variables, avoid committing secrets, redact logs and outputs, and rotate any key that may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/html-designer-paid)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON containing HTML/CSS code, design recommendations, configuration steps, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command suggestions and file changes when the host agent grants read, write, or execution tools.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
