## Description:

Import documents and retrieve knowledge through the Keystone REST API for file, URL, and Markdown uploads; hybrid search; cross-knowledge-base search; and browsing imported knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justaboyhai-wq](https://clawhub.ai/user/justaboyhai-wq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an agent to Keystone knowledge bases, import documents or URLs, create Markdown knowledge, browse entries, and retrieve grounded context with hybrid search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access Keystone knowledge bases with an API key and supports import, edit, and delete actions.

Mitigation: Use a least-privilege Keystone API key, confirm the target knowledge base before uploads or edits, and review delete requests before approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justaboyhai-wq/skills/keystone)
- [Publisher profile](https://clawhub.ai/user/justaboyhai-wq)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, API request examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KEYSTONE_BASE_URL and KEYSTONE_API_KEY for live Keystone API use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
