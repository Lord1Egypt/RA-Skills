## Description:

Publishes local Markdown notes with image paths through a user-configured MCP publishing backend and returns a note_id lookup without creating content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dqsjqian](https://clawhub.ai/user/dqsjqian)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to automate the final publishing step for prepared image-text notes from local Markdown files and image paths. It is intended for workflows where the user supplies and trusts a compatible publishing backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured publishing backends can receive draft text and local image paths.

Mitigation: Use only localhost or audited HTTPS backends that you trust, and avoid sensitive drafts or private image paths.

Risk: Running the publishing script can post live content from the user's account.

Mitigation: Check login state first and test with non-production accounts before batch publishing.

Risk: The skill depends on a user-supplied backend with no bundled platform implementation.

Mitigation: Confirm the backend exposes the expected publishing tools and review its behavior before connecting production accounts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dqsjqian/skills/note-publisher)
- [Publisher Profile](https://clawhub.ai/user/dqsjqian)
- [README](README.md)
- [Skill Definition](SKILL.md)
- [Example Configuration](config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run a local publishing script that emits status text and a NOTE_ID after successful publication.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
