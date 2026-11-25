## Description:

Use PlaceCall to call US businesses to find places, make or change bookings, ask questions, get quotes, or follow up, then return the outcome and transcript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voygr](https://clawhub.ai/user/voygr)

### License/Terms of Use:

MIT

## Use Case:

Agents use PlaceCall to find and contact US businesses about reservations, appointments, availability, prices, quotes, orders, or other questions. The skill returns call outcomes and transcripts.

### Deployment Geography for Use:

United States (excluding Indiana, Louisiana, Minnesota, Montana, and Nebraska)

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious and its scan partial, citing possible API key exposure in chat and delayed disclosure of sign-up terms and potential key replacement.

Mitigation: Review the sign-up and key-handling steps before use, never put the API key in prompts or chat, and confirm the effect of replacing a key.

Risk: Calls reach real people and are recorded; transcripts and recordings are retained for 90 days.

Mitigation: Confirm the number and brief before dialing, ensure the recording notice fits the call, and include only information needed for the task.

## Reference(s):

- [Project page](https://github.com/voygr-tech/placecall)
- [API deprecations](https://api.voygr.tech/docs/placecall/deprecations/)
- [Credits](references/credits.md)
- [Errors](references/errors.md)
- [Gotchas](references/gotchas.md)
- [Call items](references/items.md)
- [MCP tools](references/mcp-tools.md)
- [Opening notice and recording](references/opening-notice.md)
- [Call results](references/results.md)
- [Safety](references/safety.md)
- [Sign-up](references/sign-up.md)
- [Place suggestions](references/suggest.md)

## Skill Output:

**Output Type(s):** [Text, Structured data, Call transcripts]

**Output Format:** [Call outcomes, place suggestions, and transcripts in structured responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a labeled call outcome and transcript; place searches return ranked suggestions.]

## Skill Version(s):

6.7.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
