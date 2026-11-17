## Description:

This skill helps agents create, search, update, publish, unpublish, and organize Help.Center knowledge base articles through the Help.Center API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shyjal](https://clawhub.ai/user/shyjal)

### License/Terms of Use:

MIT

## Use Case:

External developers, support teams, and documentation maintainers use this skill to manage Help.Center articles and categories from an AI agent while preserving existing content and keeping publication decisions explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live Help.Center content, including publishing, unpublishing, deleting articles, and changing categories.

Mitigation: Use draft-only workflows by default, require previews or diffs before updates, and explicitly confirm publish, unpublish, delete, and category changes.

Risk: API credentials may grant broad content permissions if the same key is used for every action.

Mitigation: Use the narrowest Help.Center API key scopes needed for the task and avoid sharing long-lived secrets in chat history.

Risk: Image upload examples accept local file paths, which can expose unintended files if paths are not reviewed.

Mitigation: Upload only user-approved files and confirm the path and purpose before invoking image upload commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shyjal/skills/helpcenter)
- [Publisher profile](https://clawhub.ai/user/shyjal)
- [Help.Center](https://help.center)
- [Help.Center API base URL](https://api.help.center)
- [Agent Skills specification](https://agentskills.io/specification.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash curl commands, JSON request bodies, and HTML article content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Help.Center API requests that create drafts, update content, publish or unpublish articles, manage categories, update metadata, and upload images.]

## Skill Version(s):

1.0.0 (source: server release and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
