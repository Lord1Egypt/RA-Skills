## Description:

Query real-time shipping status for mainstream EU/US carriers (UPS, FedEx, USPS, DHL, Royal Mail, PostNL, etc.) by tracking number.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhongkedy-del](https://clawhub.ai/user/zhongkedy-del)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to identify a likely carrier from a tracking number, query Track123 for shipment status, and receive a concise delivery summary with recent tracking events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Track123 API key could be exposed if pasted into chat or written into SKILL.md.

Mitigation: Store TRACK123_API_KEY in a protected environment variable or secret store, and do not save the key in the skill file or conversation history.

Risk: Tracking numbers sent to Track123 may reveal shipment activity and delivery metadata.

Mitigation: Query only tracking numbers the user is authorized to track, and treat returned shipment details as sensitive delivery information.

Risk: Carrier identification is pattern-based and can be ambiguous for some tracking numbers.

Mitigation: Ask the user to confirm the carrier or check multiple plausible carriers before presenting a final status.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhongkedy-del/skills/logistics-tracker-en)
- [Track123 API](https://www.track123.com/api)
- [Track123 import endpoint](https://api.track123.com/gateway/open-api/tk/v2/track/import)
- [Track123 query endpoint](https://api.track123.com/gateway/open-api/tk/v2/track/query)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls]

**Output Format:** [Markdown tracking summaries with optional bash commands and parsed API response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tracking history is presented most-recent first and truncated to 10 events when many events are returned.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
