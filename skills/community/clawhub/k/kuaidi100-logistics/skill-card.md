## Description:

Kuaidi100 Logistics helps an agent query shipment tracking, identify carriers, estimate shipping fees, and estimate delivery times through the Kuaidi100 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterlcm](https://clawhub.ai/user/peterlcm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support agents use this skill to answer logistics questions, including shipment status, carrier identification, shipping cost estimates, and expected delivery times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shipment tracking numbers, phone numbers, addresses, routes, timestamps, and logistics history may be sent to Kuaidi100.

Mitigation: Use the skill only when sharing those shipment details with Kuaidi100 is acceptable, and avoid sensitive personal or business shipments unless API key and logging risks have been reviewed.

Risk: The skill is written to trigger proactively for casual logistics requests, which can reduce user control over when shipment data is shared.

Mitigation: Prefer explicit invocation and confirm sensitive shipment details before making third-party API calls.

Risk: Free quota exhaustion can interrupt logistics queries when no API key is configured.

Mitigation: Configure KUAIDI100_API_KEY for expected production use and provide clear user guidance when quota is exhausted.

## Reference(s):

- [Kuaidi100 API base endpoint](https://api.kuaidi100.com/stdio)
- [Kuaidi100 API open platform](https://api.kuaidi100.com)
- [ClawHub skill page](https://clawhub.ai/peterlcm/skills/kuaidi100-logistics)
- [ClawHub publisher profile](https://clawhub.ai/user/peterlcm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline bash curl examples and API-returned Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include third-party logistics API responses and guidance for configuring KUAIDI100_API_KEY.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
