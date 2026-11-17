## Description:

Translates PDF documents and arXiv papers while preserving layout by extracting content, translating text, and reconstructing documents with LaTeX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[overdue-lin](https://clawhub.ai/user/overdue-lin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and document authors use this skill to translate local PDFs or arXiv papers while keeping layout, figures, math, citations, and bibliography structure as intact as possible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote arXiv source archives may contain untrusted files that are extracted and later compiled locally.

Mitigation: Run arXiv mode in a disposable container or isolated workspace, inspect extracted sources before compilation, and keep secrets and important project files outside the workspace.

Risk: LaTeX compilation runs a local toolchain over generated or downloaded source files.

Mitigation: Compile with restricted filesystem access, keep shell escape disabled, apply timeouts, and review compilation logs before trusting the output.

Risk: Local PDF processing reads user-provided documents and writes rendered pages, extracted images, manifests, LaTeX, and PDFs to disk.

Mitigation: Use trusted documents where possible and choose an output directory that does not overlap with sensitive files.

## Reference(s):

- [LaTeX Layout Templates](references/latex_templates.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/overdue-lin/skills/pdf-translate-skill)
- [arXiv e-print source endpoint](https://arxiv.org/e-print/{arxiv_id})

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown instructions with inline shell commands, LaTeX snippets, and generated document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create page images, extracted image manifests, translated LaTeX source, compilation logs, and translated PDF files in the working directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
