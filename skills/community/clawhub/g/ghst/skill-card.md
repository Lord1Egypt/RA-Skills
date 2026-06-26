## Description: <br>
Work with Ghost blogs using the ghst CLI tool, including Ghost Admin API access for posts, pages, members, tags, newsletters, themes, stats, social web, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickludlam](https://clawhub.ai/user/nickludlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, site operators, and content teams use this skill to let an agent administer a Ghost publication through the ghst CLI. It supports content management, member operations, analytics, settings, themes, migrations, webhooks, raw API requests, and social web workflows when the required Ghost credentials are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer a Ghost publication through broad Admin API access. <br>
Mitigation: Install it only for agents that need Ghost administration, use a dedicated low-privilege staff token where possible, and review high-impact actions before approval. <br>
Risk: Ghost staff tokens and related API keys are sensitive credentials. <br>
Mitigation: Store credentials outside source control, avoid printing them in shared logs or chat, rotate leaked tokens promptly, and disable unused access. <br>
Risk: Publish, delete, bulk, import/export, webhook, settings, theme, social posting, and raw API operations can change public site state or data. <br>
Mitigation: Require explicit user approval, verify exact resource IDs or slugs before mutation, and prefer list or fetch commands before destructive actions. <br>
Risk: Runtime installation through npm or npx can resolve a different ghst package version over time. <br>
Mitigation: Pin or intentionally review the @tryghost/ghst package version and review release notes before upgrading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nickludlam/ghst) <br>
- [ghst CLI homepage](https://github.com/TryGhost/ghst) <br>
- [ghst npm package](https://www.npmjs.com/package/@tryghost/ghst) <br>
- [Skill instructions](SKILL.md) <br>
- [Authentication reference](references/auth.md) <br>
- [Editing workflow reference](references/editing.md) <br>
- [Post command reference](references/post.md) <br>
- [Page command reference](references/page.md) <br>
- [Member command reference](references/member.md) <br>
- [Raw API reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON-oriented command output, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the ghst binary plus Ghost URL and staff access token credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence and README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
