## Description: <br>
Give your agent a real phone. It dials, waits on hold, negotiates your bills, and returns a full transcript. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bojieli](https://clawhub.ai/user/bojieli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use Pine Voice to authenticate with Pine AI, place real phone calls on the user's behalf, and retrieve transcripts or outcomes for tasks such as reservations, customer-service calls, scheduling, and bill negotiation. <br>

### Deployment Geography for Use: <br>
US, Canada, Puerto Rico, United Kingdom, Australia, New Zealand, Singapore, Ireland, and Hong Kong <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send sensitive account, payment, or identity details to a remote voice service during real phone calls. <br>
Mitigation: Confirm the phone number, purpose, exact information to disclose, spending or account-change limits, maximum duration, and sensitive-data boundaries before initiating a call. <br>
Risk: The skill can place real calls without a clear final approval checkpoint. <br>
Mitigation: Require explicit user approval of the complete call plan and destination number immediately before running the call command. <br>
Risk: Credentials persist locally in ~/.pine-voice/credentials.json after authentication. <br>
Mitigation: Use the stored credentials only for intended calls and delete ~/.pine-voice/credentials.json when the user no longer wants the skill authenticated. <br>


## Reference(s): <br>
- [Pine Voice ClawHub Listing](https://clawhub.ai/bojieli/pine-voice) <br>
- [Pine AI](https://19pine.ai) <br>
- [Pine AI Privacy Policy](https://www.19pine.ai/page/privacy-policy) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Text, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request or response bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, one-time email authentication, and locally stored Pine Voice credentials.] <br>

## Skill Version(s): <br>
1.2.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
