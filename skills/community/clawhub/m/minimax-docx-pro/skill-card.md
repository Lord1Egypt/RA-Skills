## Description:

Enterprise-grade Word document generation. Creates validated .docx files with professional formatting, visual hierarchy, and cross-application compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luaqnyin](https://clawhub.ai/user/luaqnyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-producing agents use this skill to create, rebuild, inspect, and validate professional Word documents, including template-based updates and from-scratch document generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically download and run a .NET installer and write persistent files under ~/.dotnet.

Mitigation: Preinstall the required .NET runtime or remove the auto-provisioning path before deployment in environments where network installation or persistent home-directory writes are not acceptable.

Risk: Audit and template-apply workflows inspect or extract user-supplied DOCX archives.

Mitigation: Run DOCX processing in a sandbox with archive extraction limits, especially for untrusted documents or shared worker environments.

## Reference(s):

- [MiniMax DOCX Pro on ClawHub](https://clawhub.ai/luaqnyin/skills/minimax-docx-pro)
- [Create Workflow](guides/create-workflow.md)
- [Template Apply Workflow](guides/template-apply-workflow.md)
- [Document Input Normalization Protocol](guides/doc-input-normalization.md)
- [Document Visual System](guides/styling.md)
- [Troubleshooting Guide](guides/troubleshooting.md)
- [Mapping Schema](schemas/mapping.schema.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline shell commands and generated DOCX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces validated Word documents and may emit mapping JSON, previews, diagnostics, and audit results during document generation workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
