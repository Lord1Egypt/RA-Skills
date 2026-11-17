## Description:

Manage Google Tag Manager containers, tags, triggers, variables, and versions via the GTM API v2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonfunk](https://clawhub.ai/user/simonfunk)

### License/Terms of Use:


## Use Case:

Developers, engineers, and marketing operations teams use this skill to inspect and manage Google Tag Manager containers, workspaces, tags, triggers, variables, versions, and publishing workflows through the GTM API v2.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live or destructive Google Tag Manager changes, including deletes and publishing container versions.

Mitigation: Use a least-privilege Google identity limited to the intended containers, review all JSON before upload, and require human confirmation before delete or publish operations.

Risk: Version creation has a local code-injection issue when untrusted name or notes values are passed.

Mitigation: Avoid running create-version with untrusted name or notes values until the injection issue is fixed.

## Reference(s):

- [GTM API v2 Quick Reference](references/api-reference.md)
- [GTM Recipes JSON Templates](references/recipes.md)
- [ClawHub skill page](https://clawhub.ai/simonfunk/skills/google-tag-manager)
- [Google Tag Manager API v2 base endpoint](https://tagmanager.googleapis.com/tagmanager/v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference GTM account, container, workspace, tag, trigger, variable, version, and service account credential settings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
