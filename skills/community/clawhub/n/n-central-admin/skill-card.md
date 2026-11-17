## Description:

Operate N-able N-central safely and efficiently through its web UI. Use when handling device administration, filters, rules, scheduled tasks, automation policies, monitoring associations, remote tools, and tenant/customer/site scoped changes in N-central.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blake-lucas](https://clawhub.ai/user/blake-lucas)

### License/Terms of Use:


## Use Case:

External operators and managed services administrators use this skill to guide safe N-able N-central web UI administration for device management, filters, rules, scheduled tasks, automation policies, monitoring, and scoped tenant changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: N-central administration can affect production tenants, sites, devices, rules, scheduled tasks, and endpoint tools.

Mitigation: Require explicit customer, site, device, or tenant scope; confirm target counts before saving; run pilots before broad rollout; and keep audit notes.

Risk: Command, patch, backup/export, registry, file, service, and process actions can have high operational impact.

Mitigation: Reserve these actions for authorized maintenance or incident workflows, verify role permissions, and validate outcomes on a small sample before expanding scope.

Risk: Filter, rule, or task targeting can be broader than intended, especially when using bulk selectors or filter snapshots.

Mitigation: Prefer narrow scopes and explicit device shortlists, preview filter membership, confirm effective target lists, and clone shared objects before making risky changes.

## Reference(s):

- [UI Navigation and Operating Model](references/ui-navigation-and-operating-model.md)
- [Filters and Rules](references/filters-and-rules.md)
- [Automation Policies and Scheduled Tasks](references/automation-policies-and-tasks.md)
- [Device Details Tabs and Tools](references/device-details-tabs-and-tools.md)
- [Browser Operator Playbooks](references/browser-operator-playbooks.md)
- [ClawHub Skill Page](https://clawhub.ai/blake-lucas/skills/n-central-admin)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands]

**Output Format:** [Markdown guidance with step-by-step operating procedures and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve customer, site, device, and change scope and include validation or audit checkpoints for high-impact actions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
