## Description:

Analyzes webpage HTML structure, identifies interactive elements, and helps generate Selenium automation code for authorized pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icestorms](https://clawhub.ai/user/icestorms)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect authorized webpages, inventory form controls and links, and draft Selenium automation scripts for workflows such as login, search, and form submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive page HTML, including tokens or credentials, when page source is saved or sent for model analysis.

Mitigation: Use only on public or explicitly authorized pages, avoid internal or sensitive pages, redact HTML before model submission, and delete temporary HTML files after analysis.

Risk: The browser automation script has broad page access and disables certificate-error handling in the bundled fetch workflow.

Mitigation: Run in an isolated environment, restrict target URLs before use, validate TLS instead of ignoring certificate errors, and use browser sandboxing.

## Reference(s):

- [HTML-to-Selenium ClawHub skill page](https://clawhub.ai/icestorms/skills/html-to-selenium)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with element inventory tables, Python Selenium code, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or handle local HTML files and page element summaries.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
