## Description: <br>
Handle errors and logging following project conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laimiaohua](https://clawhub.ai/user/laimiaohua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add API exception handling, validation errors, resource-not-found handling, logging, and frontend error-response conventions for projects that use ApiException patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logs can expose secrets or sensitive personal data if the guidance is applied without filtering. <br>
Mitigation: Avoid logging passwords, tokens, full card numbers, and other sensitive values; review log fields before deployment. <br>
Risk: The examples assume a project that provides tkms ApiException and the documented response format. <br>
Mitigation: Use this skill only in codebases that follow those conventions or adapt the examples to the local exception and response APIs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laimiaohua/gi-error-handling) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, markdown] <br>
**Output Format:** [Markdown guidance with Python and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable install behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
