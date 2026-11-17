## Description:

IMA Skills helps agents manage IMA notes and knowledge bases through IMA OpenAPI, including note search, note creation, knowledge-base search, file upload, URL import, and source-content retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iampennyli](https://clawhub.ai/user/iampennyli)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent search, browse, create, and append IMA notes, and to add, browse, search, or retrieve content from IMA knowledge bases. The skill is intended for users who provide their own IMA OpenAPI Client ID and API Key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags credential and update-handling risks for a skill that uses user-provided IMA OpenAPI credentials.

Mitigation: Constrain network access to ima.qq.com and *.myqcloud.com, keep credentials in a secret manager or protected files, and avoid custom base URLs.

Risk: Update instructions returned by the service may be untrusted text.

Mitigation: Require explicit user review and confirmation before following any service-returned update instruction.

Risk: Write operations can create or append notes and upload files to a knowledge base.

Mitigation: Confirm ambiguous note targets, validate UTF-8 text before note writes, run upload preflight checks, and stop if COS upload fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iampennyli/skills/ima-skills)
- [IMA](https://ima.qq.com)
- [IMA OpenAPI credential setup](https://ima.qq.com/agent-interface)
- [IMA knowledge-base API reference](knowledge-base/references/api.md)
- [IMA notes API reference](notes/references/api.md)
- [Tencent Cloud COS request signature reference](https://cloud.tencent.com/document/product/436/7778)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or later and user-provided IMA OpenAPI credentials for live API operations.]

## Skill Version(s):

1.1.7 (source: server release evidence and artifact meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
