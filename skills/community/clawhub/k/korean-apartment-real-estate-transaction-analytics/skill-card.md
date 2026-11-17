## Description:

Provides OpenClaw access to Korean apartment transaction lookup and analysis by region, transaction type, and period through the Everyhouse real-estate service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[novb1492](https://clawhub.ai/user/novb1492)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to request Korean apartment transaction information and analytics for supported regions by providing a region, date range, and transaction type. Optional district, neighborhood, and apartment-name inputs narrow the lookup.

### Deployment Geography for Use:

Global; data coverage is limited to supported South Korean regions.

## Known Risks and Mitigations:

Risk: Search inputs are sent to everyhouse-real-payment.com and the full request URL is logged locally.

Mitigation: Use only the required real-estate search fields and avoid entering sensitive personal notes or unrelated private information.

Risk: Results depend on an external real-estate API and may be incomplete, unavailable, or unsuitable as the sole basis for a transaction decision.

Mitigation: Treat returned analytics as informational and verify important figures against authoritative real-estate or government records before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/novb1492/skills/korean-apartment-real-estate-transaction-analytics)
- [npm package @brokimyeah/openclaw-eho](https://www.npmjs.com/package/@brokimyeah/openclaw-eho)
- [Everyhouse real-payment service](https://www.everyhouse-real-payment.com/?si=%EC%84%9C%EC%9A%B8&sn=0)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [OpenClaw text response containing request parameters and the upstream API response, with JSON pretty-printed when returned by the service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires sido, typeDetail, start, and end; optional gu, dong, and apt narrow the lookup.]

## Skill Version(s):

1.1.13 (source: ClawHub server release evidence; artifact package.json is 1.1.6 and openclaw.plugin.json is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
