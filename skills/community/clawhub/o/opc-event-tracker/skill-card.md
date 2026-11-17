## Description:

追踪 OPC、AI 和独立开发者相关赛事活动，从信息源抓取赛事信息，提取结构化字段，并可在用户启用上传后提交到 OPC 公共赛事池。

This skill is ready for commercial/non-commercial use.

## Publisher:

[guipi888](https://clawhub.ai/user/guipi888)

### License/Terms of Use:

MIT

## Use Case:

External users and agent operators use this skill to discover, track, summarize, and optionally publish OPC, AI, hackathon, startup, and independent developer event records. It supports local Markdown/JSON tracking, source management, and OPC event-pool query or ingest workflows that require a locally configured API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store an OPC API key locally and use it for event-pool query or ingest requests.

Mitigation: Keep the key in the local user_config.json file, do not publish that file, and use the skill only if local API-key storage is acceptable.

Risk: When upload is enabled, scraped event records may be submitted to a public OPC event pool.

Mitigation: Keep upload_enabled false unless public publication is intended, and review event fields before enabling or running ingest workflows.

Risk: Changing api_base or adding untrusted event sources can send the API key or scraped data outside the intended service.

Mitigation: Keep api_base fixed to https://mrkjai.com and add only trusted HTTPS event sources after reviewing what they fetch and submit.

## Reference(s):

- [OPC API specification](references/api-spec.md)
- [Platform event source guide](references/platform-spec.md)
- [Source management and parser guide](references/sources-mgmt.md)
- [Event record templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries, local Markdown records, structured JSON history, shell command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform HTTPS fetches from configured event sources and OPC API requests when the user has configured an API key and enabled upload.]

## Skill Version(s):

2.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
