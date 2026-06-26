## Description: <br>
Generate complete automated API test cases from interface documentation such as OpenAPI, Swagger exports, Postman collections, Markdown API docs, or endpoint tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huahuaweiwei](https://clawhub.ai/user/huahuaweiwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to convert API documentation into executable test suites, configure request setup and response assertions, run the suite in a selected environment, and produce pass/fail reports with coverage notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated test suites can send real requests to user-provided APIs, including create, update, or delete operations. <br>
Mitigation: Review the base URL, credentials, pre-request scripts, and mutating cases before execution; prefer non-production environments and test tokens. <br>
Risk: Generated tests may use sensitive authentication material supplied through environment files or variables. <br>
Mitigation: Keep secrets in environment variables or approved secret files, avoid hard-coding credentials in generated cases, and confirm authorization before sending requests. <br>


## Reference(s): <br>
- [Environment Contract](references/environment-contract.md) <br>
- [Report Contract](references/report-contract.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/huahuaweiwei/my-api-test-automation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON manifests, generated test code, configuration files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate and execute API test workspaces for Postman/Newman, pytest, or a user-specified runner.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
