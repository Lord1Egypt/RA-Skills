## Description:

Helps OpenClaw agents manage Halo CMS blog posts, categories, tags, and comments through the Halo REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomasoscar](https://clawhub.ai/user/thomasoscar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to let an agent list Halo CMS content, create or publish blog posts, manage tags and categories, and reply to comments from a controlled workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a Halo CMS account and make durable content changes.

Mitigation: Use it only in a tightly controlled workspace, review requested publishing or deletion actions before execution, and use narrowly scoped revocable credentials.

Risk: Credential handling and write/delete powers are broader and less controlled than the documentation indicates.

Mitigation: Avoid parent-directory .env.halo files, pin HALO_URL to a trusted local or HTTPS Halo instance, and do not rely on the script itself to enforce publish, delete, or sensitive-content confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thomasoscar/skills/openclaw-halo-cms)
- [Publisher profile](https://clawhub.ai/user/thomasoscar)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform authenticated Halo CMS read, create, publish, reply, and recycle operations when invoked with configured credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
