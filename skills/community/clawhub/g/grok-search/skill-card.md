## Description:

Search the web or X/Twitter using xAI Grok server-side tools (web_search, x_search) via the xAI Responses API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[notabhay](https://clawhub.ai/user/notabhay)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve web results, X/Twitter posts, citations, Grok chat responses, and available xAI model information through local Node scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, search queries, filters, and explicitly supplied images are sent to xAI when the bundled scripts are run.

Mitigation: Use the skill only for data that is acceptable to share with xAI, and avoid secrets, private documents, and sensitive images.

Risk: Broad trigger phrases may invoke the skill when xAI API use is not intended.

Mitigation: Narrow or review triggers before deployment in environments where accidental third-party API calls are a concern.

Risk: The optional raw debug mode can expose full API payloads in stderr.

Mitigation: Avoid `--raw` unless debugging in an environment where logs are controlled.

## Reference(s):

- [xAI Search tools](https://docs.x.ai/docs/guides/tools/search-tools)
- [xAI Tools overview](https://docs.x.ai/docs/guides/tools/overview)
- [xAI API reference](https://docs.x.ai/docs/api-reference)
- [xAI tools docs quick links](references/xai-tools-links.md)
- [ClawHub skill page](https://clawhub.ai/notabhay/skills/grok-search)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown instructions with shell commands; script output is JSON, plain text, or citation URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output includes query, mode, results, and citations; chat output may include citations; model listing prints model identifiers or JSON.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
