## Description:

Jointly analyze a research paper and its open-source implementation. Use when a user wants to understand a paper through code, map theory/formulas/algorithms/experiments to real classes and methods, identify implementation details not disclosed in the paper, produce reproducibility commands and gaps, build explanatory diagrams or a static reader, or validate that an analysis covers both the paper and repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-narcissus](https://clawhub.ai/user/c-narcissus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and engineers use this skill to connect a paper's claims, formulas, algorithms, experiments, and omissions to the concrete classes, methods, parameters, commands, and logs in an open-source implementation. It produces analysis artifacts that help readers understand, reproduce, audit, and modify paper implementations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled reader builder can recursively delete an arbitrary user-writable output directory when run with a custom --out path and --force.

Mitigation: Use a fresh project directory, avoid custom --out paths, and use --force only when the output is the expected generated site directory.

Risk: Installing KaTeX fonts requires CDN access.

Mitigation: Use --install-katex-fonts only when external CDN access is acceptable for the workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/c-narcissus/skills/paper-code-joint-analysis)
- [Output Contract](references/output-contract.md)
- [Analysis Bundle Schema](references/analysis-bundle.schema.json)
- [Reader Data Contract](references/reader-data-contract.md)
- [Deep Reading Overlay](references/deep-reading-overlay.md)
- [Large Artifact Policy](references/large-artifact-policy.md)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON analysis bundle, Mermaid diagrams, reproducibility commands, and generated static reader files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default user-facing reports are in Chinese unless the user requests another language; technical identifiers remain in their original form.]

## Skill Version(s):

1.0.9 (source: evidence release metadata and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
