## Description:

Extracts text from images and PDFs, including scanned PDF pages, PDF tables, and batches of documents, with results organized for copying or saving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to extract readable text and Markdown tables from uploaded images, PDFs, scanned documents, and folders of mixed PDF/image files. It is useful for document digitization, report/table extraction, notes, citations, and content reuse when the user accepts the RedFox API-key and vision-processing requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary rates the release as suspicious because it requires a RedFox API key and performs a remote permission check before local processing.

Mitigation: Review before installing, use a revocable RedFox API key, confirm the key source and scope, and avoid exposing the key in prompts, logs, code, or output files.

Risk: Document pages or images may be handled by the agent's vision tooling, which can be inappropriate for confidential or regulated documents.

Mitigation: Avoid confidential documents unless external vision processing is acceptable for the use case and workspace policy.

Risk: The skill can create local OCR page images and Markdown output files, while the security summary notes that file-writing behavior is understated.

Mitigation: Run the skill in a constrained workspace, choose output directories deliberately, review generated files, and remove temporary OCR images when they are no longer needed.

Risk: The skill depends on local Python packages and processes user-selected files or directories.

Mitigation: Use pinned dependencies where possible and limit execution to trusted files and expected directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/image-text-extractor)
- [RedFoxHub skills](https://redfox.hk/skills)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance, files]

**Output Format:** [Markdown text, JSON extraction results, and optional local Markdown or rendered image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PDF tables are emitted as Markdown tables; scanned pages and image inputs can be listed for agent vision processing.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact frontmatter reports 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
