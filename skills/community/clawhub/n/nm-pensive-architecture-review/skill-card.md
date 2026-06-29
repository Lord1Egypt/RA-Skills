## Description: <br>
Assesses architecture decisions, ADR compliance, and coupling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review system design changes, refactors, new modules, dependency restructuring, ADR compliance, coupling, invariants, and architectural trade-offs before merging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers such as architecture, design, ADR, coupling, patterns, and principles may activate the skill during general design discussions. <br>
Mitigation: Disable the skill or narrow triggers when architecture review should run only on explicit review requests. <br>
Risk: The skill can produce architectural recommendations that may be incomplete or unsuitable for a specific repository context. <br>
Mitigation: Treat findings as review guidance and require human engineering review before relying on recommendations or changing design decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-pensive-architecture-review) <br>
- [Night Market pensive plugin](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>
- [FPF Framework](https://github.com/ailev/FPF) <br>
- [quint-code](https://github.com/m0n0x41d/quint-code) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with checklists, diagrams, tables, recommendations, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ADR audit results, coupling analysis, invariant conflict options, principle checks, risk summaries, and follow-up actions.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
