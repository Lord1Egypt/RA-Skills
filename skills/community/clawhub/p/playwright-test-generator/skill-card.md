## Description:

Generates Playwright Page Object Models, standard test scripts, data-driven tests, and locator data from natural language descriptions, HTML, or page URLs for pytest-playwright, Jest Playwright, and native Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and test automation specialists use this skill to bootstrap Playwright tests, Page Object Models, and locator sets from natural language, HTML snippets, or trusted page URLs before reviewing and adapting the generated code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can browse arbitrary URLs during page analysis.

Mitigation: Use mock or trusted test URLs, avoid internal or production systems, and review generated outputs before running them in CI.

Risk: Generated executable tests may include unescaped or incorrect data from user input, HTML, or page content.

Mitigation: Review and edit generated tests before execution, especially when inputs include untrusted HTML or test data.

Risk: Dependencies may become outdated or differ from the reviewed artifact state.

Mitigation: Pin and update dependencies deliberately before installation or CI use.

## Reference(s):


## Skill Output:

**Output Type(s):** [code, files, configuration, guidance]

**Output Format:** [Markdown, source code, JSON locator data, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated test code should be reviewed before execution, especially when derived from URLs, HTML, or user-provided test data.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact package.json and setup.py report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
