## Description:

Parse PDF documents with MinerU MCP to extract text, tables, and formulas. Supports multiple backends including MLX-accelerated inference on Apple Silicon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etoile04](https://clawhub.ai/user/etoile04)

### License/Terms of Use:


## Use Case:

Developers and document-processing users use this skill to parse PDFs or supported image files into structured Markdown with extracted text, tables, formulas, metadata, and optional persisted output files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs mutable third-party code through uvx.

Mitigation: Pin and review the mcp-mineru package version before use, and run it in an isolated environment.

Risk: The test script can turn untrusted arguments into executable Python.

Mitigation: Do not run test.sh with untrusted input; prefer the direct parser interface with validated file paths and numeric page arguments.

Risk: Parsed documents may contain sensitive or unauthorized content.

Mitigation: Use only documents the operator is authorized to process and choose output directories appropriate for the document sensitivity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/etoile04/skills/mineru-pdf)
- [MinerU MCP repository](https://github.com/TINKPA/mcp-mineru)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration]

**Output Format:** [Structured Markdown text with optional persisted Markdown files and extracted image assets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports page ranges, backend selection, table and formula toggles, and persistent output directories.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
