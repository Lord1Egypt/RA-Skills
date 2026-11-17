## Description:

Execute PowerShell commands reliably on Windows. Avoid &&, handle parameter parsing, recover from interruptions, and ensure cross-session continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalomeve](https://clawhub.ai/user/dalomeve)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to produce reliable Windows PowerShell command patterns, including safer command sequencing, parameter handling, path handling, output encoding, retries, and checkpoint-based recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checkpoint files can expose sensitive progress state if scripts include secrets or credentials.

Mitigation: Store only non-sensitive progress fields in checkpoint files, exclude password, token, secret, API key, and credential values, and keep checkpoints local to the working directory.

Risk: PowerShell snippets copied from guidance may perform unintended local actions if run without review.

Mitigation: Review generated commands before execution, use explicit error handling, and treat examples as templates to adapt to the local environment.

## Reference(s):

- [Privacy Security Checklist](references/privacy-checklist.md)
- [Microsoft PowerShell documentation](https://docs.microsoft.com/powershell)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local execution patterns, safety checklists, and reviewable PowerShell snippets; no bundled executable payload.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
