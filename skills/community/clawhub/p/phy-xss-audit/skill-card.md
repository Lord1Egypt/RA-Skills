## Description:

Cross-Site Scripting (XSS) static vulnerability scanner for JavaScript/TypeScript, React, Vue, Angular, Python/Django/Jinja2, PHP, Ruby/ERB, and Go html/template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to run a local static scan for reflected, stored, and DOM-based XSS patterns and receive prioritized findings with remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recursive scanning can follow symlinks and read files outside the selected project.

Mitigation: Run it only on trusted workspaces or remove symlinks from the target tree before scanning, especially in CI.

Risk: The scanner reads local source files and may print short matching code snippets in its findings.

Mitigation: Treat reports and CI logs as sensitive when scanning private code.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-xss-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands]

**Output Format:** [Markdown reports, JSON findings, GitHub annotations, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CI mode can exit non-zero when critical or high findings are detected.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
