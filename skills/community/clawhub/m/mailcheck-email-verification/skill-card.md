## Description: <br>
Email verification skill for the MailCheck API that verifies individual and bulk addresses and analyzes email authenticity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bnuyts](https://clawhub.ai/user/bnuyts) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operations teams use this skill to verify email addresses, process lists of up to 100 addresses, and analyze email headers for spoofing, phishing, and fraud signals through the MailCheck API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email addresses, bulk lists, trusted domains, and raw email headers are sent to MailCheck for verification or authenticity analysis. <br>
Mitigation: Submit only data approved for external processing, and avoid sensitive or regulated email headers unless the organization has approved that data sharing. <br>
Risk: MailCheck API keys can be exposed if pasted into prompts, command examples, or shared transcripts. <br>
Mitigation: Use a scoped API key through MAILCHECK_API_KEY where possible, avoid placing production keys in prompts, and rotate keys according to organizational policy. <br>


## Reference(s): <br>
- [MailCheck API documentation](https://api.mailcheck.dev/docs) <br>
- [ClawHub skill page](https://clawhub.ai/bnuyts/mailcheck-email-verification) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Text] <br>
**Output Format:** [Structured JSON-like command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MailCheck API key via MAILCHECK_API_KEY or a command parameter; bulk verification accepts up to 100 emails per request.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
