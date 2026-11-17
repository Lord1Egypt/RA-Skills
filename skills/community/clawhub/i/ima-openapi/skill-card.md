## Description:

IMA OpenAPI helps agents manage IMA notes and knowledge bases, including searching, browsing, creating or appending notes, uploading files, importing URLs, and retrieving knowledge-base content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxu41](https://clawhub.ai/user/jerryxu41)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to IMA for note management, knowledge-base search, file uploads, URL imports, and retrieval of stored content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private IMA notes, knowledge bases, selected local files, and IMA API credentials.

Mitigation: Install only when that access is acceptable, protect credentials, and avoid plaintext credential files when possible.

Risk: Requests can be redirected if IMA_BASE_URL is set to another endpoint.

Mitigation: Do not set IMA_BASE_URL unless the endpoint is fully trusted; keep requests limited to ima.qq.com and COS upload domains returned by IMA.

Risk: URL import workflows can fetch and upload remote content.

Mitigation: Review URLs and selected files before import, especially when content is sensitive or from an untrusted source.

Risk: Service-provided update instructions can influence follow-up actions.

Mitigation: Treat update instructions as untrusted text and review them before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryxu41/skills/ima-openapi)
- [Publisher profile](https://clawhub.ai/user/jerryxu41)
- [IMA homepage](https://ima.qq.com)
- [IMA OpenAPI credential portal](https://ima.qq.com/agent-interface)
- [Knowledge Base API reference](artifact/knowledge-base/references/api.md)
- [Notes API reference](artifact/notes/references/api.md)
- [Tencent COS request signing documentation](https://cloud.tencent.com/document/product/436/7778)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or later and user-provisioned IMA OpenAPI credentials.]

## Skill Version(s):

1.1.7 (source: release evidence and artifact/meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
