## Description: <br>
Genetic algorithm optimizer for AI agents that supports multi-objective Pareto optimization for portfolio weights, pricing, hyperparameters, marketing mix, and other nonlinear search problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure and call OraClaw Evolve for nonlinear or combinatorial optimization problems with multiple competing objectives. It is suited for tradeoff analysis such as portfolio optimization, marketing mix modeling, hyperparameter tuning, and pricing optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optimization inputs are sent to the OraClaw service using ORACLAW_API_KEY. <br>
Mitigation: Install only if the user trusts the OraClaw service with the optimization inputs provided. <br>
Risk: Large or repeated optimizations may incur paid usage. <br>
Mitigation: Confirm the intended run size and cost expectations before high-generation or repeated calls. <br>


## Reference(s): <br>
- [OraClaw Evolve homepage](https://oraclaw.dev/evolve) <br>
- [ClawHub skill listing](https://clawhub.ai/whatsonyourmind/oraclaw-evolve) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of ORACLAW_API_KEY and optimize_evolve parameters; the external service returns best chromosome, Pareto frontier, convergence generation, and execution time.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
