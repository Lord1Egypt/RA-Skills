## Description:

Virtual gene knockout simulation using foundation models to predict transcriptional changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Bioinformatics developers and computational biology teams use this skill to run virtual gene knockout workflows, prioritize target genes, and generate simulated differential expression, pathway, ranking, visualization, and validation-planning outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Simulated target rankings, p-values, pathway results, and validation guidance may be mistaken for validated biological findings.

Mitigation: Treat generated biological results as simulated output and require independent scientific validation before using them for research, clinical, or wet lab decisions.

Risk: The workflow executes Python code and installs scientific dependencies that may change behavior across environments.

Mitigation: Install and run the skill in an isolated environment, pin dependencies before installation, and review generated files before sharing or acting on them.

Risk: The artifact presents production-ready language while the implementation uses placeholder model inference and simulated statistics.

Mitigation: Replace placeholder logic with verified model inference and validation datasets before relying on outputs for decision support.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/in-silico-perturbation-oracle-1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and Python workflow artifacts; when run, the script writes CSV, JSON, PNG, and text files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include differential expression tables, pathway enrichment data, target score rankings, visualization plots, combinatorial screening results, and optional wet lab validation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
