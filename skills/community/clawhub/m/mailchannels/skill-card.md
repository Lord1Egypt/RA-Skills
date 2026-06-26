## Description: <br>
Send email via MailChannels Email API and ingest signed delivery-event webhooks into Clawdbot (Moltbot). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ttulttul](https://clawhub.ai/user/ttulttul) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure MailChannels email sending, domain authentication, and delivery-event webhook handling for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to send real email using MailChannels credentials. <br>
Mitigation: Use a dedicated or scoped API key where possible and require explicit approval before production sends. <br>
Risk: Delivery-event webhooks could be spoofed or misattributed if signature and account checks are skipped. <br>
Mitigation: Enforce webhook signature verification, reject stale signatures, and require customer_handle to match MAILCHANNELS_ACCOUNT_ID. <br>
Risk: Raw delivery events can contain recipient and delivery-status data. <br>
Mitigation: Avoid retaining raw events longer than needed and deduplicate retries before updating delivery state. <br>


## Reference(s): <br>
- [MailChannels Email API documentation](https://docs.mailchannels.net/email-api/) <br>
- [ClawHub skill page](https://clawhub.ai/ttulttul/mailchannels) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with environment variables, endpoint references, and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAILCHANNELS_API_KEY and MAILCHANNELS_ACCOUNT_ID; curl is the referenced command-line dependency.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
