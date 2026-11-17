## Description:

AI Word form filling auto-fills .docx forms, questionnaires, surveys, and templates using reference documents, a knowledge base, or web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viverglow](https://clawhub.ai/user/viverglow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to fill Word forms and due-diligence, compliance, survey, application, or checklist documents from user-provided files, knowledge bases, or web search. It can also create and populate LLMFill knowledge bases for later form-answer retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected forms and knowledge-base files are sent to llmfill.com for processing and storage.

Mitigation: Use the skill only when document upload is authorized; avoid confidential, regulated, or internal-only material unless the user has approved the transfer.

Risk: The aif_ API token is a long-lived credential.

Mitigation: Keep the token out of chat, logs, screenshots, shell history, backups, and repositories; store it with restrictive local permissions and delete/recreate it if exposed.

Risk: Deleting remote knowledge-base or result data may be unrecoverable.

Mitigation: Confirm destructive operations before execution and keep local source copies before deleting remote files, knowledge bases, or result batches.

## Reference(s):

- [LLMFill Skill README](artifact/README.md)
- [Document Filling API](artifact/references/api-documents.md)
- [Knowledge Base API](artifact/references/api-knowledge.md)
- [Account and Configuration](artifact/references/api-account.md)
- [curl Operation Guide](artifact/references/curl-guide.md)
- [Error Codes](artifact/references/errors.md)
- [ClawHub Skill Page](https://clawhub.ai/viverglow/skills/llmfill)
- [LLMFill Service](https://www.llmfill.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output; the invoked service produces filled .docx files and optional zip downloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports human-readable and --json CLI output, asynchronous polling status, estimated and actual cost fields, and downloaded result paths.]

## Skill Version(s):

1.0.8 (source: server release metadata and README version notes)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
