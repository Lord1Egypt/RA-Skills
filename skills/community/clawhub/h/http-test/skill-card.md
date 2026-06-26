## Description: <br>
Build reusable HTTP API test artifacts from user-provided endpoints, authentication, request data, expected results, and validation rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[may4748854-rgb](https://clawhub.ai/user/may4748854-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to turn ad hoc HTTP/REST checks into reusable .http test cases and shell verification scripts that validate responses and produce readable PASS/FAIL reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate and run shell scripts that make HTTP requests to user-provided endpoints. <br>
Mitigation: Inspect generated scripts before execution and run them only against intended test or authorized endpoints. <br>
Risk: API tests may require cookies, bearer tokens, or other sensitive credentials. <br>
Mitigation: Use test or least-privilege credentials, pass secrets through environment variables, and avoid committing real tokens or cookies. <br>
Risk: Raw response saving can expose sensitive response data if paths are not controlled. <br>
Mitigation: Keep expect.save paths inside a dedicated temporary output directory and review saved payloads before sharing artifacts. <br>


## Reference(s): <br>
- [Assertion Cheatsheet](references/assertion-cheatsheet.md) <br>
- [Complex Scenarios](references/complex-scenarios.md) <br>
- [Debugging Cookbook](references/debugging-cookbook.md) <br>
- [HTTP Test Artifact Example](references/http_test_artifact_example.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/may4748854-rgb/http-test) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with generated .http test definitions and bash verification scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts may include environment-variable placeholders for credentials and optional raw response save paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
