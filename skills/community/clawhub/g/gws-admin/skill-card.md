## Description:

Google Workspace Admin SDK: Manage users, groups, and devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:


## Use Case:

Google Workspace administrators and agents use this skill to inspect and prepare Google Workspace Admin SDK CLI commands for managing users, groups, domains, organizational units, roles, tokens, verification codes, and devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes high-impact Google Workspace administration actions, including deletes, role changes, 2-Step Verification changes, token operations, verification-code access, device wipes, and user sign-outs.

Mitigation: Use a least-privilege Google account and require explicit human approval before executing destructive or security-sensitive commands.

Risk: The security evidence notes insufficient built-in safety scoping for high-impact account and security administration.

Mitigation: Prefer read-only inspection commands before mutations, inspect each method schema, and scope parameters to the exact intended user, group, domain, role, token, or device.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-admin)
- [Artifact SKILL.md](artifact/SKILL.md)
- [ChromeOS device batch status API](https://developers.google.com/workspace/admin/directory/reference/rest/v1/customer.devices.chromeos/batchChangeStatus)
- [Directory API patch semantics](https://developers.google.com/workspace/admin/directory/v1/guides/performance#patch)
- [Cloud Identity transitive membership API](https://cloud.google.com/identity/docs/reference/rest/v1/groups.memberships/checkTransitiveMembership)
- [Directory API troubleshooting](https://developers.google.com/workspace/admin/directory/v1/guides/troubleshoot-error-codes)
- [Cloud Identity Devices API overview](https://cloud.google.com/identity/docs/concepts/overview-devices)
- [Directory API users update](https://developers.google.com/workspace/admin/directory/v1/reference/users/update)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and Google Workspace administrative credentials configured by the related gws shared setup.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
