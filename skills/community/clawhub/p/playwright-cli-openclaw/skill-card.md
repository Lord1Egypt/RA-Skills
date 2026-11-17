## Description:

Provides Playwright CLI guidance for browser automation across Chromium, Firefox, and WebKit, including page navigation, element interaction, screenshots, PDF generation, operation recording, and test workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michael-c-matias](https://clawhub.ai/user/michael-c-matias)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to operate Playwright CLI workflows for browser automation, screenshots, PDF generation, code recording, and end-to-end test execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Playwright automation can affect websites or accounts beyond the user's authorization.

Mitigation: Use the skill only for sites and accounts the user is authorized to automate.

Risk: Global package installs, browser dependency installs, or install-deps commands can modify the execution environment.

Mitigation: Install Playwright in a project-local or virtual environment with pinned versions where practical, and review the impact before using admin-level dependency installs.

Risk: Authentication state files, screenshots, PDFs, and generated scripts can contain credentials or sensitive page data.

Mitigation: Avoid hardcoding real passwords and protect auth.json, screenshots, PDFs, and generated scripts as sensitive files.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of local screenshots, PDFs, auth state files, and generated automation scripts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
