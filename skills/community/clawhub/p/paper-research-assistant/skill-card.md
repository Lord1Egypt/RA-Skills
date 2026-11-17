## Description:

Paper Research Assistant helps agents parse research papers, extract metadata and contributions, generate structured reading reports, locate code and dataset resources, scaffold reproduction code, and design experiments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[limax666](https://clawhub.ai/user/limax666)

### License/Terms of Use:


## Use Case:

Researchers, developers, and engineering teams use this skill to analyze papers and plan reproductions. It summarizes PDFs or paper links, creates reading reports, checks code and dataset availability, and drafts experiment scaffolds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted paper title or metadata value could cause the scaffold generator to write files outside the selected output directory.

Mitigation: Sanitize generated directory names, verify every output path remains under the chosen output directory, and run the generator in a sandbox or disposable workspace.

Risk: Generated reports and reproduction scaffolds can contain incomplete or misleading research guidance if paper parsing or resource discovery is wrong.

Mitigation: Use trusted paper metadata, manually verify extracted claims, links, licenses, datasets, and generated files before relying on or executing the outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/limax666/skills/paper-research-assistant)
- [Report Template](artifact/report_template.md)
- [Code Style Guide](artifact/code_style.md)
- [Experiment Design Guide](artifact/experiment_design.md)
- [CMU Experiment Design Reference](https://www.cs.cmu.edu/~aarti/Class/10701/experiment_design.pdf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON metadata, Python scaffold code, shell commands, and configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports and code scaffolds should be reviewed and adapted before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
