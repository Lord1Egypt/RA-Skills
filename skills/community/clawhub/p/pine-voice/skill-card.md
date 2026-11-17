## Description:

Give your agent a real phone. It dials, waits on hold, negotiates your bills, and returns a full transcript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bojieli](https://clawhub.ai/user/bojieli)

### License/Terms of Use:


## Use Case:

External users and agents use Pine Voice to place English-language phone calls through Pine AI for tasks such as customer-service negotiations, reservations, appointment scheduling, and follow-up calls, then review the returned transcript and call outcome.

### Deployment Geography for Use:

Supported calling countries and regions: United States, Canada, Puerto Rico, United Kingdom, Australia, New Zealand, Singapore, Ireland, and Hong Kong.

## Known Risks and Mitigations:

Risk: The skill can send phone numbers, call instructions, call context, and transcripts to Pine AI servers.

Mitigation: Use it only for calls where that disclosure is acceptable, and provide the minimum context needed for the call objective.

Risk: Call context may include sensitive account, payment, or verification details.

Mitigation: Avoid passwords, CVVs, full payment-card numbers, banking credentials, security-question answers, and one-time codes unless disclosure has been separately approved.

Risk: A local Pine Voice access token is stored at ~/.pine-voice/credentials.json.

Mitigation: Keep local file permissions restricted, review access to the host account, and remove the credentials file when the skill no longer needs access.

Risk: The call APIs in the artifact point to a staging hostname.

Mitigation: Review the endpoint before installation or use, and confirm that staging infrastructure is appropriate for the intended release.

Risk: The voice agent cannot ask the user for missing information during a live call, which can cause failed or inaccurate call outcomes.

Mitigation: Collect required callee context, account details, constraints, and success criteria before placing a call, then evaluate the transcript rather than relying only on status fields.

## Reference(s):

- [Pine Voice ClawHub listing](https://clawhub.ai/bojieli/skills/pine-voice)
- [Pine AI homepage](https://19pine.ai)
- [Pine AI privacy policy](https://www.19pine.ai/page/privacy-policy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON call parameters, JSON call status responses, and returned transcript text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js. Authentication writes a local Pine Voice credentials file, and completed calls can return transcript, duration, and credits charged.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
