## Description:

Use CallMyCall API to start, end, and check AI phone calls, and return results in chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benjaminwaye](https://clawhub.ai/user/benjaminwaye)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to place, end, monitor, and retrieve results for CallMyCall AI phone calls from an OpenClaw chat session after reviewing the call details and confirming execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound calls can contact the wrong person, caller ID, emergency, or premium number.

Mitigation: Review phone number, caller ID, call goal, and call brief before confirmation; validate E.164 formatting and block emergency or premium numbers before execution.

Risk: Recordings, transcripts, phone numbers, and call goals may contain sensitive personal data.

Mitigation: Show transcript excerpts only on explicit request, warn before exposing recording URLs, and apply consent and retention controls appropriate to the call.

Risk: The CallMyCall API key can be exposed if copied into source files, chat output, logs, or call state.

Mitigation: Keep the API key in an environment variable or user config, do not echo it, and do not store it in skill files or recent call state.

Risk: Optional webhooks and PII fields can send sensitive data to destinations the user did not intend.

Mitigation: Avoid optional webhooks and PII fields unless the user has a clear need and trusts the destination.

Risk: A scheduled-call request could be mistaken for an autonomous background job.

Mitigation: Prepare only an in-session call plan and require the user to return and explicitly confirm execution; do not create cron, launchd, task scheduler, or background runs.

## Reference(s):

- [CallMyCall API portal](https://api.callmycall.com)
- [CallMyCall API Reference](references/api.md)
- [Auth and Config](docs/auth-config.md)
- [Event Updates for Pull-Based CallMyCall](docs/event-updates.md)
- [Example Prompts](examples/prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration guidance]

**Output Format:** [Markdown status summaries, call plans, and concise call result text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CALLMYCALL_API_KEY and explicit user confirmation before placing outbound calls.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
