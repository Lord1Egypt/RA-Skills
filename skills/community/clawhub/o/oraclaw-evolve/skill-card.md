## Description:

Oraclaw Evolve helps AI agents run genetic algorithm optimization for multi-objective problems such as portfolio weights, pricing, hyperparameters, and marketing mix across nonlinear search spaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use Oraclaw Evolve to submit multi-objective optimization jobs for nonlinear, discontinuous, or combinatorial problems such as portfolio allocation, marketing mix, pricing, and ML hyperparameter tuning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an ORACLAW_API_KEY and charges per optimization request.

Mitigation: Confirm the API key and payment terms before use, and monitor optimization volume for cost control.

Risk: Optimization inputs are sent to OraClaw's service.

Mitigation: Avoid submitting sensitive financial or business data unless OraClaw's service terms and data handling meet the deployment requirements.

Risk: Genetic algorithm results are approximate and may vary with generations, mutation rate, and selection or crossover settings.

Mitigation: Review convergence statistics and the Pareto frontier, then tune parameters or rerun jobs before relying on results for consequential decisions.

## Reference(s):

- [Oraclaw Evolve Homepage](https://oraclaw.dev/evolve)
- [ClawHub Skill Page](https://clawhub.ai/whatsonyourmind/skills/oraclaw-evolve)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, JSON]

**Output Format:** [Markdown instructions with JSON parameter examples and optimization result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ORACLAW_API_KEY; paid per optimization; returns best chromosome, Pareto frontier, convergence generation, and execution time.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
