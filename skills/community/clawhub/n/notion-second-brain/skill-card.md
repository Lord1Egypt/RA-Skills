## Description:

Files messages from Telegram into the user's Notion second brain — books, fleeting notes, tasks — consistently and without clarifying questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prakhar728](https://clawhub.ai/user/prakhar728)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to capture short Telegram-style messages into a Notion Second Brain workspace, routing books, tasks, resources, references, and thoughts into the appropriate Notion database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation words can cause unrelated Telegram messages to be captured into Notion.

Mitigation: Review activation words before installation and narrow them if accidental captures would be costly.

Risk: Low-confidence captures may be written without a clarification step.

Mitigation: Review the Notion Inbox and Reading List after capture, and share the Notion integration only with the intended Second Brain page.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration guidance]

**Output Format:** [Short text confirmations, markdown field content, and structured Notion page payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes to existing Notion Reading List and Inbox databases after locating the user's Second Brain workspace; does not create missing workspace structure.]

## Skill Version(s):

0.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
