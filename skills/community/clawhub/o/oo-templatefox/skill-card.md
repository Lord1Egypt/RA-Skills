## Description:

TemplateFox (templatefox.com). Use this skill for ANY TemplateFox request — reading, creating, and updating data. Whenever a task involves TemplateFox, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill with a connected TemplateFox account to inspect templates and account details, generate images or PDFs, and perform PDF operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup executes remote installer code that was not inspected and may add persistent changes across agent applications.

Mitigation: Review the CLI installation and any bundled skills separately; prefer a reviewed, version-pinned installation and inspect the resulting agent changes.

Risk: Documents supplied for processing pass through OOMOL, and PDF operations may consume credits, including operations labeled as reads.

Mitigation: Use only documents appropriate to send through OOMOL, and confirm the credit cost of PDF operations before running them.

## Reference(s):

- [TemplateFox API documentation](https://templatefox.com/docs/api-reference)
- [TemplateFox homepage](https://templatefox.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Text]

**Output Format:** [CLI commands with JSON request payloads and JSON or text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses vary by action and may include account or template data and signed download URLs.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
