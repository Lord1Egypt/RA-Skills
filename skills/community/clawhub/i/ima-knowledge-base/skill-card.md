## Description:

Tencent IMA knowledge base skill that helps agents use OpenAPI and browser-cookie authentication for knowledge base management, note CRUD operations, RAG question answering, folder operations, and subscribed knowledge base management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect to Tencent IMA knowledge bases, create and update notes, retrieve knowledge base content, and run knowledge-base-backed question answering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use browser cookies and API keys that grant access equivalent to an active Tencent IMA session.

Mitigation: Use a test account or limited credentials, avoid passing cookies directly in shell commands, and rotate any exposed API keys.

Risk: Some included tests and examples can create, append, update, or organize notes and folders in a live knowledge base.

Mitigation: Review request bodies before running scripts and avoid executing write tests against important knowledge bases.

Risk: Session cookies may be stored in plaintext environment files by the supplied helper scripts.

Mitigation: Store secrets in a managed secret store when possible and remove plaintext cookies after validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golngod/skills/ima-knowledge-base)
- [Tencent IMA](https://ima.qq.com)
- [Tencent IMA OpenAPI](https://ima.qq.com/openapi)
- [IMA knowledge base guide](artifact/README_KnowledgeBase.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Tencent IMA endpoints and may create, append, or update notes when users run the supplied scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
