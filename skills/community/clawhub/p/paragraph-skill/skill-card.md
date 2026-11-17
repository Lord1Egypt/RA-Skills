## Description:

OpenClaw skill for Paragraph.com Web3-native blogging with tokenization, onchain storage, and community features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claireaicodes](https://clawhub.ai/user/claireaicodes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, DAOs, and Web3 teams use this skill to let an agent publish Paragraph posts, retrieve publication and feed data, manage subscribers, and inspect tokenized post data through the Paragraph API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish posts immediately and manage subscriber actions through the connected Paragraph account.

Mitigation: Require human review of post content, newsletter sends, and subscriber changes before invoking write tools.

Risk: A custom PARAGRAPH_API_BASE_URL could transmit credentials or subscriber data to an untrusted API host.

Mitigation: Keep the default Paragraph API host unless the alternate host is explicitly trusted and reviewed.

Risk: Subscriber CSV imports read a local file path and upload contact data.

Mitigation: Use only reviewed local CSV files and do not let untrusted prompts or documents choose csvPath values.

Risk: Published Paragraph posts may become public and onchain before final URLs are available.

Mitigation: Approve the final Markdown and intended publication before creation, then verify the resulting post after onchain processing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/claireaicodes/skills/paragraph-skill)
- [Paragraph API Reference](https://paragraph.com/docs/api-reference)
- [Paragraph OpenAPI Spec](https://raw.githubusercontent.com/paragraph-xyz/paragraph-sdk-js/main/openapi.json)
- [Paragraph SDK](https://github.com/paragraph-xyz/paragraph-sdk-js)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, API calls, configuration, guidance]

**Output Format:** [JSON tool responses and submitted Markdown content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PARAGRAPH_API_KEY and PARAGRAPH_PUBLICATION_SLUG; create-post results may omit final slug or URL until onchain processing completes.]

## Skill Version(s):

1.2.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
