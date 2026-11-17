## Description:

Minimax Docx creates validated .docx files with professional formatting, visual hierarchy, and cross-application compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krisliu16](https://clawhub.ai/user/krisliu16)

### License/Terms of Use:


## Use Case:

Developers and document authors use this skill to create or update distribution-ready Word documents from scratch or from user-provided templates while preserving structure, validating OOXML output, and checking for residual placeholders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic .NET provisioning can download and execute Microsoft-hosted installer scripts.

Mitigation: Prefer preinstalling .NET manually, or review and disable automatic provisioning before using the skill on important workstations or CI runners.

Risk: Runtime repair behavior can remove the user-level .NET directory when the local installation appears corrupted.

Mitigation: Review cleanup behavior before use and test runtime repair paths in a controlled environment.

Risk: Untrusted DOCX templates may carry document-processing risk.

Mitigation: Use trusted templates, inspect inputs before template-apply workflows, and run audit and residual checks before distribution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krisliu16/skills/minimax-docx)
- [Create Workflow](artifact/guides/create-workflow.md)
- [Template-Apply Workflow](artifact/guides/template-apply-workflow.md)
- [DOC Input Normalization Protocol](artifact/guides/doc-input-normalization.md)
- [C# OpenXML Coding Guide](artifact/guides/development.md)
- [Document Visual System](artifact/guides/styling.md)
- [Troubleshooting Guide](artifact/guides/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [DOCX files with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are expected to pass audit and residual-placeholder checks before distribution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
