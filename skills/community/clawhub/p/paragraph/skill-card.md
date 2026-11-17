## Description:

OpenClaw skill for Paragraph.com, a Web3-native blogging platform with tokenization, onchain storage, and community features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claireaicodes](https://clawhub.ai/user/claireaicodes)

### License/Terms of Use:

ISC

## Use Case:

Developers, creators, DAOs, and Web3 teams use this skill to let OpenClaw agents publish Markdown posts to Paragraph, manage publication subscribers, retrieve posts and publication metadata, and inspect tokenized post data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Paragraph API key can publish public posts and manage subscribers.

Mitigation: Use an intended, scoped API key, verify the target publication, and review generated content before creating posts or sending newsletters.

Risk: A configurable PARAGRAPH_API_BASE_URL could send credentials to a non-official API host.

Mitigation: Keep PARAGRAPH_API_BASE_URL unset or pinned to https://public.api.paragraph.com/api.

Risk: Subscriber imports process email addresses and wallet addresses from local CSV files.

Mitigation: Import only intentional, verified CSV paths and confirm consent and welcome-email settings before upload.

## Reference(s):

- [Paragraph API Reference](https://paragraph.com/docs/api-reference)
- [Paragraph](https://paragraph.com)
- [Paragraph OpenAPI Spec](https://raw.githubusercontent.com/paragraph-xyz/paragraph-sdk-js/main/openapi.json)
- [Paragraph SDK](https://github.com/paragraph-xyz/paragraph-sdk-js)

## Skill Output:

**Output Type(s):** [API calls, JSON, Markdown, Configuration guidance]

**Output Format:** [Tool responses as { success, data, error } objects; post content accepts Markdown and subscriber imports accept CSV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PARAGRAPH_API_KEY and PARAGRAPH_PUBLICATION_SLUG; uses Node.js 19+ native fetch with no external npm dependencies.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter, package.json, evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
