## Description:

Search Web - CN helps Openclaw and Trae users run web search and question answering through a Volcengine web Q&A agent API.

This skill is for research and development only.

## Publisher:

[alexjunanjing-2](https://clawhub.ai/user/alexjunanjing-2)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent users can use this skill to ask current-information questions from Openclaw or Trae and receive a web-grounded answer with references, follow-up suggestions, and token usage details. It is positioned as a China-accessible alternative to Brave Search for Chinese-language search workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User queries and bearer credentials are sent to an external API provider.

Mitigation: Use the skill only with provider-approved data, and do not submit secrets, private source code, internal URLs, or regulated data unless the endpoint is approved for that data.

Risk: The script can fall back from VOLCENGINE_SEARCH_API_KEY to a broader VOLCENGINE_ARK_API_KEY.

Mitigation: Provide a dedicated, low-privilege VOLCENGINE_SEARCH_API_KEY for this skill and avoid exposing general-purpose Volcengine Ark credentials in the runtime environment.

Risk: The server security review marked the release suspicious because the external query and credential handling are under-disclosed.

Mitigation: Review the skill before installation or deployment and document the external API behavior for users who may send sensitive prompts.

## Reference(s):

- [Volcengine web Q&A agent API documentation](https://www.volcengine.com/docs/85508/1510834?lang=zh)
- [ClawHub skill release page](https://clawhub.ai/alexjunanjing-2/skills/openclaw-skill-search-web)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Console text with answer content, reference listings, optional follow-up questions, token usage, and error details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VOLCENGINE_SEARCH_API_KEY and VOLCENGINE_SEARCH_BOT_ID; can stream responses when invoked with --stream.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
