## Description:

Remember and retrieve visual content from conversations, including images, charts, diagrams, screenshots, websites, and visually similar past content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horisky](https://clawhub.ai/user/horisky)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agent operators use this skill to give an OpenClaw agent persistent visual memory for images, charts, diagrams, website screenshots, and keyword-based recall across conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images and captured webpages may be sent to the configured vision provider and persisted in local visual memory.

Mitigation: Avoid private dashboards, authenticated pages, intranet URLs, credentials, and sensitive screenshots unless the configured provider and local storage are approved for that data.

Risk: URL capture can access arbitrary targets without network safety bounds.

Mitigation: Review or patch URL restrictions before use, especially for localhost, cloud metadata addresses, intranet hosts, and other sensitive network locations.

Risk: Persisted memory summaries can contain untrusted visual or page content that may later be loaded into agent context.

Mitigation: Treat memory.md as untrusted data and review it before enabling automatic session-start loading.

Risk: The Chrome fallback uses a no-sandbox flag and the dependency range is not pinned to an exact version.

Mitigation: Remove the no-sandbox fallback where possible and pin dependencies before deployment.

## Reference(s):

- [minds-eye skill page](https://clawhub.ai/horisky/skills/minds-eye)
- [horisky publisher profile](https://clawhub.ai/user/horisky)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and text summaries of stored or retrieved visual memories]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores image copies, SQLite metadata, and a generated memory.md summary under ~/.multimodal-memory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
