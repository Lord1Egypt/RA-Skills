## Description:

Imports local documents into an ima knowledge base, helps diagnose COS upload errors, and can add structured tags to Markdown cards before upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dzz-777](https://clawhub.ai/user/dzz-777)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ima knowledge base users use this skill to import local documents into personal or shared libraries, troubleshoot upload failures, and tag Markdown knowledge cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using `--print-curl` may expose temporary upload credentials if the command output is saved or shared.

Mitigation: Avoid `--print-curl` when its output could be saved or shared, and handle any printed command as sensitive credential material.

Risk: The security review is incomplete because some referenced content could not be resolved by the scanner.

Mitigation: Review the full skill and its referenced components before relying on the partial scan result.

## Reference(s):

- [ima-mcp-cos-upload on ClawHub](https://clawhub.ai/dzz-777/skills/ima-mcp-cos-upload)
- [ima](https://ima.qq.com)
- [ima knowledge base tagging specification](artifact/references/tagging-spec.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown tagging guidance and shell commands for document import]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides an upload workflow and optional structured tags for Markdown cards.]

## Skill Version(s):

1.4.1 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
