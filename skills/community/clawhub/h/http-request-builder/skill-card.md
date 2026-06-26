## Description: <br>
Build and test HTTP requests with CLI interface: headers, auth, body, cookies, with history and templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Derick001](https://clawhub.ai/user/Derick001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers can use this skill to build, send, save, and replay HTTP requests from a terminal while testing REST APIs or debugging request behavior. It supports command-line and interactive workflows with headers, Basic or Bearer authentication, request bodies, cookies, templates, and request history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved templates and request history can contain bearer tokens, cookies, headers, request bodies, or other sensitive data in plaintext local files. <br>
Mitigation: Avoid production credentials and private payloads; inspect saved JSON files before sharing or committing them, and clear ~/.http-request-builder/history.json after sensitive requests. <br>
Risk: The security evidence marks the release suspicious because secret-bearing request data may be stored without strong warnings or redaction. <br>
Mitigation: Review before installing and treat ~/.http-request-builder/templates/ and ~/.http-request-builder/history.json as secret-bearing storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Derick001/http-request-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text output and JSON files for saved templates and request history] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends HTTP requests, prints response status, headers, and body, and stores reusable request templates and recent request history under ~/.http-request-builder/.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
