## Description:

Access and manage Web3-native blogging on Paragraph.com with onchain posts, tokenized content, subscriber management, and automated publishing via API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claireaicodes](https://clawhub.ai/user/claireaicodes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, DAOs, and Web3 project teams use this skill to let agents publish Markdown posts, inspect Paragraph publications, manage subscribers, and retrieve tokenized post and coin data through the Paragraph API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish posts and manage subscribers on a live Paragraph account.

Mitigation: Require human confirmation before post creation, subscriber changes, newsletter sending, or bulk imports.

Risk: A broad Paragraph API key could expose publishing and subscriber operations beyond the intended workflow.

Mitigation: Use a narrowly scoped API key and rotate it if it is exposed or no longer needed.

Risk: Changing PARAGRAPH_API_BASE_URL could send credentials or content to an unintended endpoint.

Mitigation: Leave PARAGRAPH_API_BASE_URL unset unless testing with non-production credentials.

Risk: CSV subscriber import reads a local file and can trigger outreach.

Mitigation: Import only from a user-approved path after confirming file contents, and set sendWelcomeEmail to false unless outreach is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/claireaicodes/skills/paragraph-test)
- [Paragraph API Reference](https://paragraph.com/docs/api-reference)
- [Paragraph OpenAPI specification](https://raw.githubusercontent.com/paragraph-xyz/paragraph-sdk-js/main/openapi.json)
- [Paragraph SDK](https://github.com/paragraph-xyz/paragraph-sdk-js)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Structured tool responses, Markdown content, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Paragraph API key and publication slug; post creation and subscriber actions can change live Paragraph account state.]

## Skill Version(s):

1.2.0 (source: server release, target metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
