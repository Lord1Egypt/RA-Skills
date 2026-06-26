## Description: <br>
Test API endpoints and document responses. Define tests in plain English, run them, get formatted results. Agent-driven Postman alternative. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and API engineers use this skill to define API tests in plain English, run user-configured HTTP requests, chain response values between tests, and produce documented test results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends real HTTP requests to endpoints configured by the user, including mutating methods such as POST, PUT, PATCH, and DELETE. <br>
Mitigation: Prefer staging or test accounts, review mutating tests before running them against production, and confirm endpoint targets before execution. <br>
Risk: Test headers and bodies may contain secrets, personal data, or production credentials. <br>
Mitigation: Avoid real secrets or personal data unless necessary, use scoped test credentials, and keep sensitive values out of reusable examples and reports. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/TheShadowRose/openclaw-api-tester) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown, YAML examples, JavaScript code, and structured API test results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can summarize pass/fail counts, response times, per-test checks, and generated reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
