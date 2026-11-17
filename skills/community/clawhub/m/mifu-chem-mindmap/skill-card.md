## Description:

Generates structured chemistry knowledge-system mind maps by turning lesson-prep content into JSON-backed, printable three-layer HTML diagrams with equation and completeness validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abill6688](https://clawhub.ai/user/abill6688)

### License/Terms of Use:

MIT-0

## Use Case:

External educators and chemistry content developers use this skill to create printable classroom and review mind maps for chemistry modules, keeping lesson-prep equations, topic structure, and rendered HTML aligned through a JSON-to-render-to-validate workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can carry unsafe content from input data.

Mitigation: Use only trusted JSON inputs, review generated HTML before sharing, and escape HTML/SVG content before handling untrusted data.

Risk: Validation results may overstate safety or correctness.

Mitigation: Manually review equations with skipped parsing, rendered output counts, conditions, phenomena, and classroom content before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abill6688/skills/mifu-chem-mindmap)
- [Structure standard](references/01-structure-standard.md)
- [Design specification](references/02-design-spec.md)
- [Verification specification](references/03-verification.md)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON data structures, command-line examples, validation output, and generated printable HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated HTML is intended to be zero-dependency and printable; trusted inputs and human review remain required.]

## Skill Version(s):

1.0.0 (source: server release metadata and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
