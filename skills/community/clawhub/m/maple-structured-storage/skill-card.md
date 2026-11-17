## Description:

Archives unstructured reports, notes, and knowledge documents into structured topic folders with indexing, retrieval, and reflection prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chentx1243](https://clawhub.ai/user/chentx1243)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and knowledge workers use this skill to convert pasted text or Markdown/text files from a configured source folder into a structured local knowledge archive. It refreshes an index, retrieves relevant topics, preserves code snippets, and asks targeted follow-up questions when context is missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The archive may store credentials, private endpoints, personal data, or proprietary material in plaintext.

Mitigation: Review and redact source content before archiving, use a dedicated archive folder, and avoid broad project or home directories.

Risk: The workflow can move processed source files and write follow-up answers back into archive files.

Mitigation: Confirm source and storage paths before use, preview important content manually, and keep backups for source material that should not be moved or rewritten.

## Reference(s):

- [File Writing Rules](artifact/references/file-rules.md)
- [Reflection Workflow](artifact/references/reflection.md)
- [Maple Structured Storage on ClawHub](https://clawhub.ai/chentx1243/skills/maple-structured-storage)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Configuration, Guidance]

**Output Format:** [Markdown archive files, JSON index data, copied resource files, and concise conversational follow-up questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write to configured local source and storage paths, move processed source files to done/, and preserve code snippets verbatim.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
