## Description:

Tracks JD Logistics waybills, summarizes delivery status and timelines, estimates delivery windows, diagnoses common delivery exceptions, and supports batch checks for up to 10 JD waybills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuhui-xiaohe](https://clawhub.ai/user/xuhui-xiaohe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support agents use this skill to check JD Logistics waybill status, review recent tracking events, estimate delivery timing, and receive guidance for delays or delivery exceptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send JD waybill numbers and a live JD session token to JD endpoints.

Mitigation: Use only necessary headers, keep tokens short-lived, and never log, display, persist, or share JD session tokens.

Risk: Recent JD waybill numbers may be written to a local history cache without clear privacy controls.

Mitigation: Disable the cache unless needed, or enforce a small capped cache with clear retention, deletion, and local-only storage rules.

Risk: Tracking data can be delayed and the skill only supports JD-operated waybill numbers.

Mitigation: Tell users that logistics data may lag by 5-30 minutes and route non-JD or high-volume business tracking needs to the appropriate JD app or merchant tool.

## Reference(s):

- [JD Express waybill API specification](artifact/skills/jd-express-tracking/references/api-spec.md)
- [JD Logistics proxy endpoint](https://lop-proxy.jd.com)
- [ClawHub skill page](https://clawhub.ai/xuhui-xiaohe/skills/jd-express-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown tracking summaries with status cards, timeline entries, delivery estimates, and exception-handling guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May render a timeline widget and is limited to 10 JD waybills per batch request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
