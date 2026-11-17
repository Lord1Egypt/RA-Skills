## Description:

Translates natural language molecular structure queries into MolQL (Mol-Script) expressions for Mol* or compatible molecular viewers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhonghua-wang](https://clawhub.ai/user/zhonghua-wang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and molecular modeling users use this skill to convert natural-language structure selection requests into MolQL expressions for molecular viewers. It supports atom, residue, chain, distance, property, and multi-part selections, and asks clarifying questions when requests are ambiguous.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect or ambiguous natural-language selections can produce MolQL that selects unintended molecular structures.

Mitigation: Review generated MolQL against the request and ask clarifying questions for active-site, binding-pocket, or other ambiguous selections before use.

Risk: The bundled publishing helper can publish the skill using the caller's ClawHub account or token if executed intentionally.

Mitigation: Run scripts/publish.sh only when publishing is intended and after confirming the target owner, credentials, and dry-run output.

## Reference(s):

- [Mol-Script Expression Syntax Reference Manual](references/molql-syntax.md)
- [MolQL Translation Examples](references/translation-examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with MolQL Lisp code blocks and explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include clarifying questions for ambiguous molecular selection requests.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
