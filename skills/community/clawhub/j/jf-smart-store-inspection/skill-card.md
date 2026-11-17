## Description:

Guides JF smart-store setup and AI patrol operations, including store and camera onboarding, inspection plans, record analysis, and HTML reports with captured images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Store operators and integrators use this skill to onboard stores and cameras, manage AI inspection plans, review patrol records, and create visual reports for business teams.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: Starting, stopping, or deleting plans, stores, and devices changes live business operations.

Mitigation: Restrict execution to trusted operators and confirm targets before making changes.

Risk: Generated reports may render untrusted patrol data and image URLs unsafely.

Mitigation: Avoid opening or sharing reports from untrusted patrol data until HTML escaping and URL validation are fixed.

Risk: JF account credentials and sensitive patrol records may be exposed if the API host is misconfigured.

Mitigation: Use trusted account credentials and keep the endpoint set to the official API host.

## Reference(s):

- [JF Smart Store Inspection API reference](references/api-reference.md)
- [ClawHub skill listing](https://clawhub.ai/jftech/skills/jf-smart-store-inspection)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, HTML reports, Configuration]

**Output Format:** [Text and JSON responses, JSON configuration, and standalone HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include patrol details and cloud-hosted camera snapshots.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
