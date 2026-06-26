## Description: <br>
Industrial-grade scheduling and resource optimization for AI agents that solves task scheduling with energy matching, budget allocation, and LP/MIP constraint problems in milliseconds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and planning agents use this skill to solve scheduling, budget allocation, staffing, routing, capacity planning, and other constraint-based optimization problems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Schedules, budgets, staffing plans, routing data, or other optimization inputs are sent to the OraClaw service. <br>
Mitigation: Use only data the user is comfortable sharing with the service, and review sensitive inputs before calling the solver. <br>
Risk: Solver calls may consume quota or incur charges. <br>
Mitigation: Set confirmations, usage limits, or cost controls before repeated or automated use. <br>


## Reference(s): <br>
- [OraClaw Solver homepage](https://oraclaw.dev/solver) <br>
- [ClawHub skill page](https://clawhub.ai/whatsonyourmind/oraclaw-solver) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON, API Calls] <br>
**Output Format:** [Markdown guidance with JSON request examples and solver result expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ORACLAW_API_KEY; external solver calls may consume quota or incur per-call charges.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
