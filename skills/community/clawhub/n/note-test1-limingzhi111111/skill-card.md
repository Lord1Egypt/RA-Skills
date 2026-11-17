## Description:

This skill helps agents manage a user's IMA personal notes through the IMA OpenAPI, including searching notes, browsing notebooks, reading note content, creating notes, and appending Markdown content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaolibuzai-ovo](https://clawhub.ai/user/xiaolibuzai-ovo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to search, browse, read, create, and update personal IMA notes after the user configures IMA OpenAPI credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read or modify private IMA notes from broad or ambiguous prompts.

Mitigation: Use it only for explicit IMA note requests and confirm before reading note bodies, creating notes, or appending content.

Risk: Credential files may be stored in plaintext if users follow file-based setup.

Mitigation: Prefer environment variables or an OS secret store, or ensure ~/.config/ima and credential files are owner-only.

Risk: Displaying note bodies can expose sensitive personal material.

Mitigation: Show only titles and summaries in shared or group contexts unless the user explicitly authorizes disclosure.

## Reference(s):

- [IMA Note API Reference](references/api.md)
- [IMA Homepage](https://ima.qq.com)
- [ClawHub Skill Page](https://clawhub.ai/xiaolibuzai-ovo/skills/note-test1-limingzhi111111)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command and JSON API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IMA_OPENAPI_CLIENTID and IMA_OPENAPI_APIKEY credentials; note read and write operations should be scoped to explicit user requests.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
