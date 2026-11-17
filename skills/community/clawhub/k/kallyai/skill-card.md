## Description:

KallyAI Executive Assistant handles outbound and inbound calls, email, bookings, research, errands, multi-channel messaging, and phone number management on a user's behalf.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sltelitsyn](https://clawhub.ai/user/sltelitsyn)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to delegate executive-assistant tasks such as phone calls, inbound receptionist workflows, email, bookings, research, errands, outreach, budget checks, credits, subscriptions, referrals, and multi-channel messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad natural-language interface can delegate sensitive real-world actions such as calls, messages, email, bookings, billing-related tasks, and phone number changes.

Mitigation: Prefer explicit direct commands for high-impact tasks and require user confirmation before actions that spend money, contact third parties, change phone numbers, or affect accounts.

Risk: The release depends on an external CLI package that the security summary describes as unpinned.

Mitigation: Install only from a trusted source, review the package before use, and favor pinned and verifiable CLI releases when deploying.

Risk: OAuth-backed access may retain ability to operate on calls, messages, email, bookings, and related user data.

Mitigation: Use login and logout controls deliberately, check authentication status before use, and revoke stored access when the skill is no longer needed.

## Reference(s):

- [KallyAI ClawHub skill page](https://clawhub.ai/sltelitsyn/skills/kallyai)
- [KallyAI publisher profile](https://clawhub.ai/user/sltelitsyn)
- [KallyAI API base URL](https://api.kallyai.com)
- [KallyAI OAuth authorization endpoint](https://api.kallyai.com/v1/auth/authorize?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&scope=calls.write)
- [KallyAI calls API endpoint](https://api.kallyai.com/v1/calls)

## Skill Output:

**Output Type(s):** [text, shell commands, API calls, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the kallyai CLI and authenticated KallyAI account access for live actions.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
