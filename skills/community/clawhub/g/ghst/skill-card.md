## Description:

Work with Ghost blogs using the ghst CLI tool. Supports full Ghost Admin API access including posts, pages, members, tags, newsletters, themes, stats, social web (ActivityPub), and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickludlam](https://clawhub.ai/user/nickludlam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to let an agent manage Ghost blogs through the ghst CLI and Ghost Admin API, including content, members, newsletters, themes, analytics, webhooks, and migration tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify live Ghost content, settings, themes, webhooks, member data, and comments through the Ghost Admin API.

Mitigation: Use a dedicated low-privilege Ghost staff account, verify exact target IDs or slugs before mutations, and require explicit user approval before publishing, deleting, importing, exporting, changing settings, managing webhooks, or making raw API calls.

Risk: A leaked Ghost staff access token could allow unauthorized administration of the Ghost site.

Mitigation: Store GHOST_STAFF_ACCESS_TOKEN securely, keep it out of chat and version control, rotate it immediately if exposed, and remove agent access when it is no longer needed.

Risk: Floating npm or npx installs can pull an unreviewed ghst CLI version at runtime.

Mitigation: Install @tryghost/ghst from the official npm registry, pin a reviewed version for production use, and review release notes before upgrading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickludlam/skills/ghst)
- [ghst CLI homepage](https://github.com/TryGhost/ghst)
- [@tryghost/ghst npm package](https://www.npmjs.com/package/@tryghost/ghst)
- [Editing posts and pages reference](references/editing.md)
- [Raw API reference](references/api.md)
- [Authentication reference](references/auth.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may direct the agent to run ghst commands that operate on live Ghost site data and can return JSON or CSV outputs.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
