## Description:

Converts webpages into runnable Python Selenium automation scripts by fetching rendered HTML and screenshots, analyzing page structure and interactions, and producing element locators, workflow guidance, and code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icestorms](https://clawhub.ai/user/icestorms)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to inspect public or authenticated webpages and generate Selenium scripts for form filling, navigation, clicking, searching, and repeatable browser workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use supplied credentials for automated login.

Mitigation: Use it only on explicitly trusted domains, prefer least-privilege accounts, and avoid broad ROUTER_* environment credentials.

Risk: Command-line credentials and generated artifacts can expose sensitive data.

Mitigation: Do not pass real passwords on the command line, and treat screenshots, rendered HTML, and metadata files as sensitive outputs.

Risk: Generated Selenium code may perform unintended browser actions if the page analysis is wrong.

Mitigation: Review generated scripts and workflow steps before running them against real accounts or internal systems.

## Reference(s):

- [Selenium patterns](artifact/html-to-selenium/references/selenium-patterns.md)
- [Operation examples](artifact/html-to-selenium/references/examples.md)
- [Skill manifest](artifact/html-to-selenium/MANIFEST.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown with Python and shell code blocks, plus generated screenshot, HTML, and metadata files when the fetch script is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated browser artifacts may include screenshots, rendered HTML, and page metadata; generated Selenium code should be reviewed before execution.]

## Skill Version(s):

2.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
