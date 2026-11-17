## Description:

Munger Decision Free is a Chinese-language decision-analysis assistant that applies 12 Charlie Munger mental models to recommend relevant models, guide structured questioning, and generate Markdown decision reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cdz0451](https://clawhub.ai/user/cdz0451)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for educational decision support when evaluating investment, product, hiring, strategy, or life decisions. The skill helps them classify the decision scenario, select relevant mental models, answer guided questions, and produce a concise Markdown analysis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investment or allocation suggestions could be mistaken for financial advice.

Mitigation: Treat outputs as educational decision prompts and require independent review before acting on financial or allocation decisions.

Risk: Quality and dependency concerns could affect reliability in CI or development workflows.

Mitigation: Refresh vulnerable development dependencies, run the included tests, and rescan before relying on the package in automated workflows.

Risk: Examples, data files, or release metadata may not fully align with shipped behavior.

Mitigation: Verify installed package contents, required data files, and examples against the released version before deployment.

## Reference(s):

- [Mental model reference index](artifact/references/INDEX.md)
- [First Principles](artifact/references/01-08-first-principles.md)
- [Opportunity Cost](artifact/references/02-02-opportunity-cost.md)
- [Compound Effect](artifact/references/03-03-compound-effect.md)
- [Critical Mass](artifact/references/04-04-critical-mass.md)
- [Preparation and Launch](artifact/references/05-05-preparation-launch.md)
- [Circle of Competence](artifact/references/06-06-circle-of-competence.md)
- [Inversion](artifact/references/07-07-inversion.md)
- [Mental Models Lattice](artifact/references/08-08-first-principles.md)
- [Moat](artifact/references/09-09-moat.md)
- [Margin of Safety](artifact/references/10-10-margin-of-safety.md)
- [Lollapalooza Effect](artifact/references/11-11-lollapalooza-effect.md)
- [Confirmation Bias](artifact/references/12-12-confirmation-bias.md)
- [ClawHub skill page](https://clawhub.ai/cdz0451/skills/munger-decision-free)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with guided questions and final decision-analysis reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; requires Node.js when running the TypeScript implementation.]

## Skill Version(s):

1.2.4 (source: server release evidence; artifact package metadata lists 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
