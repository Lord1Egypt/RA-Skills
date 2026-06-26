## Description: <br>
Tests configured models for availability and reports pass/fail results with durations and error details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmanrui](https://clawhub.ai/user/xmanrui) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to check whether one specified model or all configured provider/model combinations are available, with a concise summary of failures for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Testing multiple configured models can consume API resources, hit rate limits, or disclose model error details in the result summary. <br>
Mitigation: Ask for a single model or confirm all-model checks first when cost, rate limits, or error-detail disclosure matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xmanrui/model-healthcheck) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text or Markdown list with status, duration, error details, and final tally] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can test one specified model or all configured models; concurrent all-model checks may consume API resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
