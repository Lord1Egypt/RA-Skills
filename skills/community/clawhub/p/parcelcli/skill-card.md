## Description:

Track parcels locally with parcelcli for Evri, Royal Mail, UPS, FedEx, and DHL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cavit99](https://clawhub.ai/user/cavit99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to track parcels locally, detect carriers, watch delivery status, and summarize normalized carrier tracking results without relying on third-party parcel aggregation services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tracking numbers, postcodes, and parcel watch state can be sensitive personal delivery data.

Mitigation: Keep tracking data local, use postcodes only when provided or explicitly requested, and remove local watches when monitoring is no longer needed.

Risk: Carrier pages may return unsupported, credential-required, timeout, or WAF failure states.

Mitigation: Report unsupported or credential-required states plainly, and retry timeout or WAF failures once later instead of looping.

## Reference(s):

- [parcelcli GitHub homepage](https://github.com/cavit99/parcelcli)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and summarized JSON fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should use normalized parcel status fields and avoid raw carrier page text.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
