## Description:

Manage Microsoft Intune and Entra ID device management through Microsoft Graph for devices, compliance, policies, apps, enrollment, reporting, audit, and related administration tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattiacirillo](https://clawhub.ai/user/mattiacirillo)

### License/Terms of Use:

MIT-0

## Use Case:

IT administrators, managed service providers, and operations teams use this skill to query and manage Microsoft Intune and Entra ID device-management resources from an OpenClaw-compatible agent. It supports read-only reporting as well as confirmed administrative changes through Microsoft Graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform high-impact tenant, policy, app, group, and device actions through Microsoft Graph.

Mitigation: Use INTUNE_READ_ONLY=true and read-only Graph permissions unless writes are specifically required; when writes are enabled, grant only the minimum Graph permissions needed.

Risk: Destructive Tier 3 actions depend partly on the agent following the typed-name confirmation process.

Mitigation: Require an operator to verify the target object, consequences, and exact confirmed name before running wipe, retire, delete, Activation Lock bypass, or Conditional Access delete actions.

Risk: The authoritative security verdict is suspicious because one documented safety gate is weaker than claimed.

Mitigation: Review the release before installing in a production tenant and prefer read-only deployment for reporting use cases.

## Reference(s):

- [OpenClaw Intune Skill ClawHub Page](https://clawhub.ai/mattiacirillo/skills/openclaw-intune-skill)
- [Kaffee & Code](https://kaffeeundcode.com)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Microsoft Graph API Docs](https://learn.microsoft.com/en-us/graph/api/resources/intune-graph-overview)
- [Users, Groups, RBAC, Terms & Notifications](references/admin.md)
- [Apps & App Protection (MAM)](references/apps.md)
- [Devices, Remote Actions, Categories, Scripts](references/devices.md)
- [Network Profiles & Windows Updates](references/network-updates.md)
- [Platform: Autopilot, Enrollment, Apple, Android Enterprise](references/platform.md)
- [Policies: Compliance, Configuration, Endpoint Security, Conditional Access, Filters](references/policies.md)
- [Reporting, Audit Logs, Settings Catalog Search, GPO Analytics](references/reporting.md)
- [Troubleshooting: Common Graph API Errors](references/troubleshooting.md)
- [Multi-Step Workflows (MSP Recipes)](references/workflows.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and summarized Microsoft Graph results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Formats results as tables or short summaries and avoids raw JSON dumps unless needed for an administrative action.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter and changelog report 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
