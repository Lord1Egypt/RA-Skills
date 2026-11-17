## Description:

Home Fix-It helps users diagnose home repair issues from photos or descriptions, classify DIY safety risk, estimate costs, generate repair guidance, and track maintenance tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

Homeowners, renters, and maintenance-minded users use this skill to triage common household repair and upkeep tasks, estimate DIY versus contractor costs, and decide when a licensed professional is required. Developers or operators can also use the included setup and dashboard materials to configure local home profiles, repair logs, appliance records, and maintenance schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privacy expectations may be unclear because local-only claims conflict with dashboard and database artifacts that can store home details and repair photos.

Mitigation: Require explicit confirmation before saving or updating files, and when using the dashboard, enforce authentication, row-level security, private image storage, and environment-secret handling.

Risk: Home repair guidance can affect physical safety when tasks involve gas, electrical panels, structural issues, asbestos, large mold areas, ladders, or powered appliances.

Mitigation: Keep RED-zone tasks as hard stops with mitigation-only guidance, tell users to call licensed professionals, and include power, water, ventilation, and safety-gear cautions for applicable YELLOW-zone tasks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nollio/skills/normieclaw-home-fix-it)
- [README](artifact/README.md)
- [Security and Safety Guarantees](artifact/SECURITY.md)
- [Safety Classification Rules](artifact/config/safety-rules.md)
- [Companion Dashboard Spec](artifact/dashboard-kit/DASHBOARD-SPEC.md)
- [Dashboard Manifest](artifact/dashboard-kit/manifest.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with numbered repair steps, safety classifications, cost estimates, setup instructions, and maintenance checklist entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local workspace files for home profiles, maintenance logs, schedules, and dashboard records when configured by the user.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
