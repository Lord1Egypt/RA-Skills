## Description:

Automate WeChat Mini Program UI operations, navigation, data validation, event listening, and screenshots inside DevTools for testing and regression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to automate WeChat Mini Program UI, E2E, and regression tests in WeChat DevTools, including navigation, element interaction, data inspection, screenshots, mocking, and audit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation can access WeChat DevTools projects, login tickets, screenshots, and test account data.

Mitigation: Use only with selected test projects or test accounts, treat tickets and screenshots as sensitive, and avoid logging or committing them.

Risk: Runtime evaluation, exposed functions, and wx method mocking can alter or inspect Mini Program behavior during tests.

Mitigation: Use evaluate, exposeFunction, and mocking APIs only in trusted test environments with reviewed snippets, and restore mocked methods after tests.

## Reference(s):

- [Full API Reference](artifact/references/api.md)
- [ClawHub skill page](https://clawhub.ai/openlark/skills/miniprogram-automator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API usage examples, DevTools setup steps, and testing workflow guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
