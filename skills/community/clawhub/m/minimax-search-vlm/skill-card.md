## Description:

Uses the MiniMax Coding Plan API to help an agent perform web search and image understanding when the user has configured a MiniMax API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l1-m1ng](https://clawhub.ai/user/l1-m1ng)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent for current web information, research assistance, and image-content analysis through MiniMax API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and images are sent to MiniMax as a third-party service.

Mitigation: Do not send confidential queries, credentials, private documents, or sensitive images unless the deployment owner has approved MiniMax for that data.

Risk: The remote-image example writes to a fixed temporary path.

Mitigation: Use a securely created temporary file path and clean it up after image analysis.

Risk: The skill depends on a locally stored MiniMax API key.

Mitigation: Store the key in the configured local file with restrictive permissions and avoid exposing it in command output or logs.

## Reference(s):

- [MiniMax Developer Platform](https://platform.minimaxi.com)
- [MiniMax Coding Plan Search API](https://api.minimaxi.com/v1/coding_plan/search)
- [MiniMax Coding Plan VLM API](https://api.minimaxi.com/v1/coding_plan/vlm)
- [ClawHub Skill Page](https://clawhub.ai/l1-m1ng/skills/minimax-search-vlm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a locally configured MINIMAX_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
