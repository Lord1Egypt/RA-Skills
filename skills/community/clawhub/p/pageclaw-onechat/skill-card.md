## Description:

One-prompt Facebook Page AI setup that connects Pages, detects business type, and loads industry-specific skills through PageClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[proship1](https://clawhub.ai/user/proship1)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and page operators use this skill to connect a Facebook Page, choose a business type, activate PageClaw-managed AI skills, and begin page-management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a PageClaw access key and may read Facebook Page conversations after the user connects a Page.

Mitigation: Install only when the user trusts PageClaw with Facebook Page-management access, and avoid exposing access keys, Page IDs, raw JSON, or other sensitive setup details.

Risk: The skill follows prompts downloaded from PageClaw that were not included in the reviewed artifact.

Mitigation: Review PageClaw's connected prompts and operational behavior before relying on the agent for live Page management.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/proship1/skills/pageclaw-onechat)
- [PageClaw](https://pageclaw.onechat.ai)
- [OneChat.ai](https://onechat.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown text with user-facing setup prompts and service-driven workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Handles PageClaw access keys and may load remote prompts after the user connects a Facebook Page.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
