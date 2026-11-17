## Description:

Parse PDFs and images into Markdown/JSON using the memect-ppx (`ppx`) CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lihanghang](https://clawhub.ai/user/lihanghang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users use this skill to run the local `ppx` CLI for OCR, PDF/image parsing, table extraction, and conversion into Markdown or JSON outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation can affect sensitive environments.

Mitigation: Use a dedicated virtual environment and review or pin package versions before installing PPX dependencies.

Risk: Backend options can send document content to configured OCR or LLM services.

Mitigation: Avoid LLM/backend options for confidential documents unless the endpoint is controlled and approved.

Risk: OCR and table extraction can produce partial or inaccurate results.

Mitigation: Inspect `doc.md`, `doc.json`, and page-level outputs, and report OCR mode, table mode, and backend choices when they affect accuracy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lihanghang/skills/memect-ppx)
- [memect-ppx homepage](https://github.com/memect/memect-ppx)
- [CLI Options](references/cli-options.md)
- [Backend Config](references/backend-config.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and references to generated Markdown/JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the output directory and notes OCR mode, table mode, and backend when relevant.]

## Skill Version(s):

0.2.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
