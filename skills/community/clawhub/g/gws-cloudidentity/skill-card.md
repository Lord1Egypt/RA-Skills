## Description: <br>
Google Cloud Identity: Manage identity groups and memberships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Google Workspace administrators use this skill to discover and draft `gws cloudidentity` CLI commands for Cloud Identity groups, memberships, devices, SSO profiles, assignments, and policies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward broad Google Workspace or Cloud Identity administrative actions beyond group management, including device wipes and SSO changes. <br>
Mitigation: Install it only for admin-capable use cases, use the least-privileged Google admin account possible, and require explicit human confirmation before wipe, delete, SSO, policy, or security-setting operations. <br>
Risk: Generated commands depend on the local `gws` binary and shared authentication instructions. <br>
Mitigation: Verify the `gws` binary and generated `gws-shared` instructions before use, then inspect each method with `gws schema` before passing parameters or JSON bodies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-cloudidentity) <br>
- [Google API resource names](https://cloud.google.com/apis/design/resource_names) <br>
- [Google Workspace multi-party approval for sensitive actions](https://support.google.com/a/answer/13790448) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the `gws` CLI binary and command inspection with `gws cloudidentity --help` or `gws schema`.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
