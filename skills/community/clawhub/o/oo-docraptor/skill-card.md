## Description:

Operate DocRaptor through an OOMOL-connected account to create hosted PDF or Excel documents from HTML or a public URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create a hosted PDF or Excel document with DocRaptor from HTML or a public URL through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup may execute remote installer code, and the installed CLI release has not been verified.

Mitigation: Install a verified oo CLI release yourself and control automatic skill synchronization before use.

Risk: Automatic synchronization may affect other agents’ skills, and the guidance does not fully explain those changes.

Mitigation: Review synchronization changes before allowing them to affect other skills.

Risk: Document content submitted to the connected service is processed by OOMOL and DocRaptor.

Mitigation: Approve document payloads and submit only content you permit both services to process.

## Reference(s):

- [DocRaptor API documentation](https://docraptor.com/documentation/api)
- [DocRaptor homepage](https://docraptor.com)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON payloads, Document download links, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON payloads; action responses include a hosted PDF or Excel download URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A hosted document is created through the DocRaptor create_hosted_document action.]

## Skill Version(s):

1.0.6 (source: skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
