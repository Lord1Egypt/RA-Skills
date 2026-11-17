## Description:

Helps developers deploy an app on their own provider accounts, with human-approved changes and verification of supported setup steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikehasa](https://clawhub.ai/user/mikehasa)

### License/Terms of Use:

MIT

## Use Case:

Developers use GoLive to plan and carry out app deployment on their own hosting and service accounts, then review verification results and remaining manual steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment actions can change live provider accounts, DNS records or production resources.

Mitigation: Review each plan and require explicit human approval, especially for live, DNS and destroy actions.

Risk: Provider credentials can grant broad access or leak through chat.

Mitigation: Use scoped, short-lived credentials where possible and never paste secrets into chat.

Risk: Local deployment state and reports can reveal account or resource details.

Mitigation: Keep state and reports out of source control and review them before sharing.

## Reference(s):

- [GoLive on ClawHub](https://clawhub.ai/mikehasa/skills/golive)
- [Planning and verification guide](artifact/references/plan-and-verify.md)
- [Guided provider setup](artifact/references/guided.md)
- [Release updates and rollback](artifact/references/updates.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON, Markdown]

**Output Format:** [Conversational guidance, JSON CLI results and Markdown deployment reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verification reports distinguish passing checks from manual or unverified steps.]

## Skill Version(s):

0.1.0-alpha.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
