## Description: <br>
Automatically routes tasks to a local or cloud AI model based on privacy, context length, cost, and performance requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keven0706](https://clawhub.ai/user/keven0706) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to choose between configured local and cloud models for each request, balancing privacy, long-context needs, cost, and performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic fallback may route non-sensitive, misclassified, long-context, or failed requests to cloud models despite privacy-oriented claims. <br>
Mitigation: Review routing rules before installation, disable cloud fallback when local-only handling is required, and test privacy-sensitive examples against the configured models. <br>
Risk: Routing audit logs record model choices, reasons, context length, privacy level, and task type. <br>
Mitigation: Set retention and access controls for audit logs, and confirm that the logged metadata is acceptable for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keven0706/multi-model-router) <br>
- [Publisher profile](https://clawhub.ai/user/keven0706) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, guidance, code] <br>
**Output Format:** [JavaScript routing result objects and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the selected model alias, migrated context, routing reason, and task analysis; writes routing audit records when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
