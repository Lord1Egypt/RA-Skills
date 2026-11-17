## Description:

基于MCP协议的高效JSON对比工具，专为AI对话场景设计，提供智能对比、快速响应和清晰输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to compare expected and actual JSON payloads through the Xiaobenyang service and present the returned diff clearly in conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JSON content and the XBY API key are sent to a third-party service.

Mitigation: Use the skill only when external processing is approved, and do not compare secrets, tokens, personal data, or proprietary records.

Risk: The API key may be persisted locally in plaintext in a .env file.

Mitigation: Keep .env out of source control, restrict filesystem access, and rotate the key if it may have been exposed.

Risk: Comparison results depend on remote API availability and correctness.

Mitigation: Review important diffs before acting on them and handle API failures as inconclusive rather than authoritative.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/jsondiff)
- [Xiaobenyang API key page](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Markdown summary of JSON comparison results, with raw JSON available from the API response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires expected and actual JSON keys and a configured XBY API key.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
