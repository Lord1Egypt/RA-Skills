## Description:

Plant Doctor helps agents identify plants from photos, diagnose plant health issues, create care cards and watering schedules, flag toxicity risks, and maintain local plant-care records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT

## Use Case:

External users and plant-care hobbyists use this skill to identify houseplants, troubleshoot symptoms from photos, receive care guidance, and track watering or care schedules in a local workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store plant details, care history, and potentially photo-derived observations in local files or memory.

Mitigation: Use it only in a private workspace, restrict access to the plants/ directory, and review any persistent-memory integration before enabling it.

Risk: The optional dashboard design may expose plant records or photos in shared or multi-user deployments if ownership, storage privacy, and access controls are incomplete.

Mitigation: Do not deploy the dashboard for multiple users until required owner fields, strict row-level security, private image storage, and cross-user access tests are in place.

Risk: Security and privacy claims in the package are not proof of protection, and the server security verdict flags the release as suspicious.

Mitigation: Treat claims as marketing, rely on independent review before deployment, and follow the server security guidance for privacy-sensitive use.

## Reference(s):

- [Plant Doctor ClawHub listing](https://clawhub.ai/nollio/skills/normieclaw-plant-doctor)
- [README](artifact/README.md)
- [Security Guidance](artifact/SECURITY.md)
- [Dashboard Companion Kit](artifact/dashboard-kit/DASHBOARD-SPEC.md)
- [Plant Care Templates](artifact/config/care-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration, files]

**Output Format:** [Markdown guidance with structured care cards, diagnosis plans, toxicity alerts, JSON plant records, and markdown care schedules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local plant collection and care schedule files under plants/ when installed and used with filesystem access.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
