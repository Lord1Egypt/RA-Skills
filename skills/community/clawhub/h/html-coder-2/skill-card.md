## Description:

HTML编码工具 helps agents build semantic HTML pages, accessible forms, responsive layouts, and interactive components.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, front-end engineers, and automation workflows use this skill to generate, review, and troubleshoot HTML pages, forms, validation behavior, and interactive components. It is scoped to HTML and front-end work rather than backend API or database design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad file and command authority could change project files or run unintended commands outside a narrow HTML task.

Mitigation: Limit use to HTML and front-end work, inspect generated diffs, and review command or deployment actions before execution.

Risk: Generated HTML or client-side scripts may introduce XSS, weak content-security controls, or sensitive-data exposure.

Mitigation: Escape and validate user-controlled input, apply an appropriate Content Security Policy, avoid hard-coded secrets, and review generated code before deployment.

Risk: API key configuration may expose credentials if secrets are pasted into prompts or committed to files.

Mitigation: Use environment variables or approved secret storage, provide credentials only for known services, and keep secrets out of generated source files and version control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/html-coder-2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-like status reports with HTML, CSS, JavaScript, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write project files or propose commands when the hosting agent grants those tools.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 2.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
