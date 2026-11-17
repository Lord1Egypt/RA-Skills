## Description:

Use this skill when the user wants to reproduce an academic paper in MATLAB from a paper file path, URL, DOI, or PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orbisz](https://clawhub.ai/user/orbisz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to turn academic papers into traceable MATLAB reproduction packages, including algorithm pseudocode, parameter audits, simulation scripts, result comparisons, and Chinese documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a self-evolution step that can store failure notes and propose changes to its own instructions.

Mitigation: Review or remove the self-evolution section before installing, and require human review for any instruction changes.

## Reference(s):

- [README](artifact/README.md)
- [Deliverables Template](artifact/references/deliverables-template.md)
- [Workflow Plan](artifact/references/workflow-plan-zh.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, MATLAB source files, parameter tables, result files, plots, and concise run guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a supplied paper, web research for cited operations, MATLAB or Octave execution, and a writable output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
