## Description: <br>
Creates a paid structured deep-dive report for a user-specified industry segment or company, covering overview, competitors, trends, opportunities, risks, and intelligence insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neo-yu3](https://clawhub.ai/user/neo-yu3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to request paid market or company research reports after order creation and payment. The agent coordinates payment status checks and produces a structured report when payment is verified. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review found that user questions and payment credentials are sent to a hard-coded backend over unencrypted HTTP. <br>
Mitigation: Avoid confidential business questions or payment flows unless the publisher updates the service to HTTPS and documents data handling and retention. <br>
Risk: The skill requests outbound network access and credential reads for a paid report workflow. <br>
Mitigation: Review the skill before installation and only run it in an environment where local order files and payment credentials can be exposed to the publisher's service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neo-yu3/industry-deep-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with payment status text and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report sections include overview, competitor landscape, trend analysis, opportunities and risks, and intelligence insights.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
