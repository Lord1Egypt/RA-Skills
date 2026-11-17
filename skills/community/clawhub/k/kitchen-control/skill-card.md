## Description:

Kitchen Control helps an OpenClaw agent process WhatsApp freezer inventory commands, update PocketBase stock and sales records, generate expiration-based schedules, and calculate dynamic pricing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m3d3l](https://clawhub.ai/user/m3d3l)

### License/Terms of Use:

MIT-0

## Use Case:

Store operators and developers can use this skill to route WhatsApp inventory, sales, and schedule commands into a PocketBase-backed freezer inventory workflow. It is intended for convenience-store freezer stock tracking, expiration-aware display planning, and sales logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WhatsApp-triggered commands can mutate inventory and sales records with administrator-backed database access.

Mitigation: Use only in a controlled environment until webhook authentication, sender-to-user authorization, and least-privileged PocketBase credentials are added.

Risk: Weak validation and non-transactional sales and inventory updates can misrecord stock or create inconsistent records.

Mitigation: Strictly validate item names, quantities, and dates, and make related inventory and sales updates transactional.

Risk: Future AI forecasting integration can become a third-party data-sharing path.

Mitigation: Document, review, or disable the forecasting integration, and limit any shared sales or inventory data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/m3d3l/skills/kitchen-control)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Plain text WhatsApp-style response strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update PocketBase inventory and sales records while returning command results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
