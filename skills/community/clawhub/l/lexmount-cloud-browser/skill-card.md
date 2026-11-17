## Description:

LexMount Cloud Browser helps an agent use LexMount's cloud browser to open pages, read content, fill and verify forms, capture screenshots, and continue work in authorized logged-in website contexts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanisk](https://clawhub.ai/user/tristanisk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when they need cloud-hosted web browsing, page inspection, form interaction, screenshots, downloads, or reuse of website login state through LexMount browser Contexts. It is suited to tasks where results should be verified from the actual page state before reporting completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cloud browser service and CLI may handle page content, screenshots, downloads, form data, and optional logged-in website contexts.

Mitigation: Install only when the user accepts LexMount service authorization, use dedicated browser Contexts for sensitive accounts, and avoid sharing credentials in chat or skill artifacts.

Risk: The skill installs a LexMount CLI binary from a remote download location during bootstrap.

Mitigation: Review CLI provenance when supply-chain control matters and rely on the bootstrap script's SHA-256 checksum verification before execution.

Risk: Browser commands can report successful execution before the intended webpage outcome is actually achieved.

Mitigation: Read back page state, verify form values, confirm screenshot or download files exist, and report the actual failure step when verification does not pass.

Risk: Read-write browser Contexts can preserve logged-in state and may conflict with parallel use or lose unsaved state if force-released.

Mitigation: Use dedicated Contexts for each account or task, close temporary sessions after work completes, and force-release only after confirming the owning session has ended.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/tristanisk/skills/lexmount-cloud-browser)
- [Authentication](references/authentication.md)
- [Commands and examples](references/commands.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown and task-specific files such as screenshots, PDFs, downloads, or command JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LexMount authorization and a platform-supported browser-cli; page actions should be verified against actual browser state before completion.]

## Skill Version(s):

1.1.18 (source: server release metadata and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
