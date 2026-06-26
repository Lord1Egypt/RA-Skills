## Description: <br>
Automates Baiwang ISP Open Platform API testing by preparing test data, signing authenticated requests, executing test cases, and generating reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squidtestgary](https://clawhub.ai/user/squidtestgary) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to run authenticated Baiwang ISP Open Platform API test suites, validate business responses, and produce local HTML and JSON reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports hardcoded credentials and possible sensitive live test data in generated local reports. <br>
Mitigation: Remove and rotate exposed credentials, replace examples with placeholders, use synthetic or masked fixture data, and restrict execution to approved test environments. <br>
Risk: The skill performs authenticated API and database-backed testing against configured environments. <br>
Mitigation: Review configuration before execution and confirm targets, database access, and credentials are approved for the intended test scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/squidtestgary/isp-api-tester) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files, Markdown] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell commands; execution produces HTML, JSON, and JavaScript report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include raw requests, responses, identifiers, tokens, or business data and should be handled as sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
