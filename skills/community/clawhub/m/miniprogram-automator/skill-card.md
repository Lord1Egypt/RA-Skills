## Description: <br>
Automate WeChat Mini Program UI operations, navigation, data validation, event listening, and screenshots inside WeChat DevTools for testing and regression. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to produce guidance, commands, and JavaScript examples for automating WeChat Mini Program tests in WeChat DevTools. It supports test flows involving page navigation, element selection and interaction, data injection, mocked wx methods, event listening, screenshots, login tickets, multi-account checks, and performance audit collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced SDK can drive WeChat DevTools, inject test code, take screenshots, and control Mini Program state. <br>
Mitigation: Use it only with trusted projects and development or QA environments where automated control is intended. <br>
Risk: Automation flows may use login tickets, test accounts, screenshots, and application data that could expose sensitive information. <br>
Mitigation: Avoid production accounts and sensitive test data; store generated screenshots and audit reports only in approved locations. <br>
Risk: The artifact requires enabling DevTools CLI/HTTP call functionality, which expands local automation access. <br>
Mitigation: Enable that setting only for controlled test workstations and disable it when automation is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/openlark/miniprogram-automator) <br>
- [Full API Reference](references/api.md) <br>
- [Publisher Profile](https://clawhub.ai/user/openlark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API usage examples and test automation setup notes; does not execute DevTools automation itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
