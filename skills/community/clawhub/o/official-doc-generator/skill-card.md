## Description:

Generates and formats formal organizational documents such as meeting minutes, speeches, discussion outlines, and work reports using GB/T 9704-2012-style formatting, template tooling, and compliance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leaproud](https://clawhub.ai/user/leaproud)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and document authors use this skill to draft, format, validate, and export formal organizational documents. It is most relevant when users need structured document types, standard formatting, template management, sensitive-word checks, or revision history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local document and template operations can overwrite or delete Word documents outside the intended template folder when unsafe names or paths are supplied.

Mitigation: Run the skill in a dedicated working folder, review output paths before execution, and reject template names with path separators, absolute paths, or `..`.

Risk: Compliance or sensitive-word suggestions may alter factual meaning or policy-sensitive wording.

Mitigation: Manually review proposed wording changes before using generated documents in formal workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leaproud/skills/official-doc-generator)
- [GB/T 9704-2012 Format Reference](artifact/references/gb_t_9704_2012_standard.md)
- [Official Language Style Guide](artifact/references/official_language_style.md)
- [Document Types Specification](artifact/references/document_types_specification.md)
- [Sensitive Words List](artifact/references/sensitive_words_list.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance, JSON configuration, Python/shell examples, Word document files, and text or JSON validation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate .docx documents, validation reports, sensitive-word check reports, template metadata, and revision history files.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
