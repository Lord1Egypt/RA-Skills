## Description:

Provides OpenClaw access to Korean apartment real transaction analysis by region, apartment, transaction type, and period.

This skill is ready for commercial/non-commercial use.

## Publisher:

[novb1492](https://clawhub.ai/user/novb1492)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can install this plugin to ask an agent for Korean apartment transaction trends and analysis using region, apartment name, transaction type, and date range. It is suited to supported South Korean regions such as Seoul, Gyeonggi, Incheon, Daejeon, Gwangju, and Daegu.

### Deployment Geography for Use:

South Korea, focused on supported regions including Seoul, Gyeonggi, Incheon, Daejeon, Gwangju, and Daegu

## Known Risks and Mitigations:

Risk: User-provided region, apartment, transaction type, and date range fields are sent to a third-party Korean real-estate service.

Mitigation: Install and use the plugin only when sending those query fields to the disclosed service is acceptable.

Risk: Behavior and data coverage are Korean-focused and limited to supported regions and available transaction records.

Mitigation: Use the skill for supported South Korean real-estate lookups and verify important results against the source service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/novb1492/skills/korean-apartment-real-transactions)
- [npm package: @brokimyeah/openclaw-eho](https://www.npmjs.com/package/@brokimyeah/openclaw-eho)
- [EveryHouse real transaction service](https://www.everyhouse-real-payment.com/?si=%EC%84%9C%EC%9A%B8&sn=0)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text responses, with JSON-formatted API data when returned by the service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries require sido, typeDetail, start, and end; gu, dong, and apt are optional.]

## Skill Version(s):

1.1.8 (source: server release metadata; artifact/package.json reports 1.1.5 and artifact/openclaw.plugin.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
