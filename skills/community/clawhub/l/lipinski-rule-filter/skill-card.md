## Description:

Filter compound libraries based on Lipinski's Rule of Five for drug-likeness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cheminformatics practitioners, and agent workflows use this skill to screen SMILES, CSV, TSV, or SDF-like compound libraries against Lipinski-style drug-likeness rules and produce reviewable pass/fail outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill executes local Python code and reads or writes user-provided compound files.

Mitigation: Run it in a least-privileged project workspace, provide explicit input and output paths, and review generated files before sharing them.

Risk: The skill depends on RDKit through rdkit-pypi, which may change behavior or supply-chain posture across installs.

Mitigation: Pin or review the RDKit dependency before automated installation, especially in production or regulated chemistry workflows.

Risk: CSV or report outputs may carry untrusted compound names from external datasets.

Mitigation: Treat generated CSV and text reports as untrusted data, sanitize them before importing into spreadsheets or downstream systems, and avoid embedding sensitive identifiers unnecessarily.

Risk: Archived audit evidence found weaker consistency for stress or boundary scenarios.

Mitigation: Keep requests within the documented Lipinski filtering scope, require clear input/output parameters, and use the documented fallback path when inputs are incomplete or execution fails.

## Reference(s):

- [Lipinski Rule of Five References](references/lipinski_references.md)
- [RDKit](https://www.rdkit.org/)
- [RDKit Documentation](https://rdkit.readthedocs.io/)
- [Lipinski Rule Filter on ClawHub](https://clawhub.ai/aipoch-ai/skills/lipinski-rule-filter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus command-line text reports and optional filtered compound files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include a single-compound rule report, filtered passed-compound files, and a companion text report summarizing failed compounds and rule violations.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
