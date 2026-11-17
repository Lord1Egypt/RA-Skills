## Description:

Virtual gene knockout simulation using foundation models to predict transcriptional changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ewankeynes](https://clawhub.ai/user/ewankeynes)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and computational biology users can use this skill to run virtual gene knockout analyses, compare predicted differential expression, inspect pathway enrichment, rank target genes, and export validation guidance. Results should be treated as exploratory decision support until model integrations and biological validation are independently verified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overstate production-grade biological foundation-model predictions while the implementation includes simulated or random placeholder behavior.

Mitigation: Treat outputs as exploratory only and do not use them for experimental, therapeutic, clinical, or business decisions unless model integrations and validation claims are independently verified.

Risk: The skill runs Python code with substantial scientific dependencies and writes generated files.

Mitigation: Install and run it in an isolated environment, pin and audit dependencies first, and keep outputs confined to a workspace directory.

Risk: Remote model or API use is not clearly documented and may involve sensitive biological data handling.

Mitigation: Assume any remote model use is sensitive until documented; avoid sending protected or confidential biological data without an approved data-handling review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ewankeynes/skills/in-silico-perturbation-oracle)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; generated analysis artifacts include CSV, JSON, PNG, and text files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes results to a user-selected output directory, including differential expression results, target scores, pathway enrichment, plots, combinatorial results, and optional validation guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
