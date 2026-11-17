## Description:

Extract and recognize text from documents, including PDF and DOCX files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fchange](https://clawhub.ai/user/fchange)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users use this skill to extract OCR text from PDF and DOCX documents through the Gitee AI document parsing API and present the extracted result in Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents or URL-fetched content may be uploaded to Gitee AI, including sensitive material.

Mitigation: Only process documents suitable for submission to Gitee AI, and review the skill before installing or running it on sensitive documents.

Risk: The script can fetch arbitrary URLs supplied through the file parameter.

Mitigation: Avoid providing URLs unless necessary, and run the skill in a restricted network environment when possible.

Risk: Supplying the API key with --api-key can expose credentials through shell history or process metadata.

Mitigation: Prefer setting GITEEAI_API_KEY through a protected environment or secret manager.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fchange/skills/moark-doc-extraction)
- [Gitee AI document parsing endpoint](https://ai.gitee.com/v1/async/documents/parse)
- [Gitee AI task status endpoint](https://ai.gitee.com/v1/task/{task_id})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown text extracted from documents, with command-line script output prefixed by EXTRACTION_RESULT.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GITEEAI_API_KEY; accepts a local document path or URL via --file.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
