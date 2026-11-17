## Description:

Configure OpenClaw semantic memory to use SiliconFlow embeddings through the OpenAI-compatible API, especially `BAAI/bge-m3`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otweihan](https://clawhub.ai/user/otweihan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure, validate, and troubleshoot OpenClaw memory_search with SiliconFlow embeddings, including curated external Markdown knowledge paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Indexed local text is sent to SiliconFlow's external embedding API.

Mitigation: Index only curated files that are appropriate to share with SiliconFlow, and avoid private journals, inboxes, secrets, generated exports, or broad repositories unless explicitly intended.

Risk: Embedding configuration requires a SiliconFlow API key.

Mitigation: Use the user's own API key and avoid placing real secrets in shared examples, logs, or public skill materials.

## Reference(s):

- [SiliconFlow OpenAI-compatible API endpoint](https://api.siliconflow.cn/v1/)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown guidance with JSON-style configuration snippets and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides validation of OpenClaw memory status, indexing, and retrieval after configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
