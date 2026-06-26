## Description: <br>
Generates complete MindStudio Run Function integrations for APIs, including Code Tab JavaScript, Configuration Tab fields, and Test Data Tab examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sol1986](https://clawhub.ai/user/Sol1986) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow builders use this skill to create MindStudio Run Function blocks that call external APIs and store results in workflow variables. It is intended for users who need ready-to-paste code, configuration, and test data for API integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated functions may call external APIs and handle credentials. <br>
Mitigation: Review the generated endpoint, request fields, and credential scope before use, and configure API keys with the least privilege required. <br>
Risk: Incorrect MindStudio input or output variable handling can produce broken workflows or write data to the wrong variable. <br>
Mitigation: Confirm inputVariable fields are read directly from ai.config and only outputVariableName fields are used as ai.vars keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sol1986/mindstudio-to-api-custom-function-builder) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Examples](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with fenced JavaScript code blocks for Code Tab, Configuration Tab, and Test Data Tab output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include a short note explaining stored variables, required configuration fields, and API-specific gotchas.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
