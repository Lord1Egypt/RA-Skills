## Description: <br>
Google Workspace Admin SDK: Manage users, groups, and devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and administrators use this skill to inspect and construct Google Workspace Admin SDK CLI commands for managing users, groups, domains, roles, devices, tokens, verification codes, and related directory resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide powerful Google Workspace account, device, domain, token, two-step verification, and role-administration actions. <br>
Mitigation: Install it only for intentional Google Workspace administration, use the narrowest possible admin and OAuth permissions, and require explicit human confirmation for destructive or privilege-changing commands. <br>
Risk: The artifact expects a shared Google Workspace skill for authentication, global flags, and security rules. <br>
Mitigation: Inspect the referenced gws-shared skill before use and generate it with gws generate-skills if it is missing. <br>


## Reference(s): <br>
- [Gws Admin ClawHub release page](https://clawhub.ai/googleworkspace-bot/gws-admin) <br>
- [Google Workspace Admin SDK ChromeOS device status](https://developers.google.com/workspace/admin/directory/reference/rest/v1/customer.devices.chromeos/batchChangeStatus) <br>
- [Google Workspace Admin SDK patch semantics](https://developers.google.com/workspace/admin/directory/v1/guides/performance#patch) <br>
- [Cloud Identity transitive membership check](https://cloud.google.com/identity/docs/reference/rest/v1/groups.memberships/checkTransitiveMembership) <br>
- [Google Workspace Admin SDK troubleshooting](https://developers.google.com/workspace/admin/directory/v1/guides/troubleshoot-error-codes) <br>
- [Cloud Identity Devices API overview](https://cloud.google.com/identity/docs/concepts/overview-devices) <br>
- [Google Workspace user update reference](https://developers.google.com/workspace/admin/directory/v1/reference/users/update) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command-parameter guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and should be used with gws admin --help and gws schema admin.<resource>.<method> before API calls.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
