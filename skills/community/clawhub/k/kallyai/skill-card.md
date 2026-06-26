## Description: <br>
KallyAI Executive Assistant handles outbound and inbound calls, email, bookings, research, errands, multi-channel messaging, and phone number management on the user's behalf. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sltelitsyn](https://clawhub.ai/user/sltelitsyn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to delegate executive-assistant tasks such as calls, email, bookings, inbox review, research, errands, outreach, credit checks, and account or subscription management. <br>

### Deployment Geography for Use: <br>
Global, subject to KallyAI-supported countries and services. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate calls, send messages, book services, spend credits, and change account settings through broad natural-language delegation. <br>
Mitigation: Require explicit confirmation before third-party contact, purchases, bookings, outreach, subscriptions, or other externally visible actions. <br>
Risk: Connected communication channels and stored tokens may expose sensitive messages, call transcripts, account data, or delegated authority. <br>
Mitigation: Review OAuth permissions, connected channels, inbound rules, active goals, and stored tokens regularly. <br>
Risk: Unbounded budgets or credit usage can cause unexpected spending. <br>
Mitigation: Set spending and booking limits, check credit balances and breakdowns, and require approval before budget increases. <br>


## Reference(s): <br>
- [KallyAI ClawHub skill page](https://clawhub.ai/sltelitsyn/kallyai) <br>
- [KallyAI API base URL](https://api.kallyai.com) <br>
- [KallyAI OAuth authorization endpoint](https://api.kallyai.com/v1/auth/authorize?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&scope=calls.write) <br>
- [KallyAI calls endpoint](https://api.kallyai.com/v1/calls) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger real-world communication, booking, spending, outreach, and account-management actions through KallyAI.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
