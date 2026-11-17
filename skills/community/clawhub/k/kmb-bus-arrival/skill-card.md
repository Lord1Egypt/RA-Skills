## Description:

Retrieve real-time KMB bus arrival information. getArrival returns plain text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenho1394](https://clawhub.ai/user/stevenho1394)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch current KMB and LWB bus arrival times by route and stop name for Hong Kong transit planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live HTTPS requests to the public KMB API.

Mitigation: Use it only in environments where outbound access to data.etabus.gov.hk is expected, and handle temporary network or service errors.

Risk: The skill depends on the certifi Python package for certificate verification.

Mitigation: Pin certifi to a reviewed version for stronger reproducibility.

## Reference(s):

- [KMB Open Data API](https://data.etabus.gov.hk/v1/transport/kmb/)
- [ClawHub skill listing](https://clawhub.ai/stevenho1394/skills/kmb-bus-arrival)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns human-readable arrivals in HKT, with up to three arrival times per matched stop.]

## Skill Version(s):

1.2.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
