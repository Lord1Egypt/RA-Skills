## Description: <br>
API Tester Pro helps agents construct and send HTTP or GraphQL requests, validate response status, headers, and bodies, and summarize latency benchmarks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to test REST and GraphQL APIs, run health checks, validate API responses, and collect basic latency benchmark results for integration or deployment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API tests can transmit tokens, credentials, private endpoints, or sensitive payloads to the selected target endpoint. <br>
Mitigation: Use only endpoints and payloads you intend to test, and avoid authenticated or private services unless that exposure is expected. <br>
Risk: Local request history can retain URLs, statuses, errors, and timing details from tests. <br>
Mitigation: Avoid including sensitive values in URLs or test names, and clear local history according to the host agent's storage controls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/534422530/laosi-api-tester) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and JSON-style API test results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe API calls to user-selected endpoints and local request-history behavior.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata, SKILL.md frontmatter, hub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
