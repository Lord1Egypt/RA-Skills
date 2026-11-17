## Description:

Publish blog posts from AI agents to WordPress via Notion. One API call handles page creation, markdown conversion, image uploads, featured image generation, and SEO metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kfuras](https://clawhub.ai/user/kfuras)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to let an agent create, update, publish, sync, and monitor blog posts through Notipo-connected Notion and WordPress accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, update, sync, and delete content in connected WordPress and Notion accounts.

Mitigation: Default to draft creation, require explicit approval before publish, update, sync, or delete operations, and review generated content before making it public.

Risk: The skill relies on a persistent API key and a Notipo endpoint supplied through environment variables.

Mitigation: Use a narrow, revocable API key and verify NOTIPO_URL is a trusted HTTPS Notipo endpoint before execution.

Risk: Global CLI installation may execute the currently resolved package version.

Mitigation: Pin or isolate the CLI installation where possible instead of installing the latest package globally.

## Reference(s):

- [Notipo API Introduction](https://notipo.com/docs/api/introduction)
- [Notipo CLI Documentation](https://notipo.com/docs/api/cli)
- [notipo npm package](https://www.npmjs.com/package/notipo)
- [ClawHub skill page](https://clawhub.ai/kfuras/skills/notipo)
- [Publisher profile](https://clawhub.ai/user/kfuras)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NOTIPO_URL and NOTIPO_API_KEY environment variables, plus access to connected Notion and WordPress accounts.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
