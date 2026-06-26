## Description: <br>
A first-principles iterative agent framework that decomposes complex goals into atomic tasks, validates intermediate results, and schedules dependency-aware execution for final delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lingxinsuixing](https://clawhub.ai/user/lingxinsuixing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to turn complex goals into first-principles task plans with dependency ordering, validation checks, and an integrated report inside OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User goals and intermediate task outputs may be routed through the host-configured LLM callable. <br>
Mitigation: Use only with an approved LLM environment, and avoid secrets, regulated data, or private customer data unless that environment is approved for them. <br>
Risk: Parsing or validation failures can produce incorrect task validation or incomplete results. <br>
Mitigation: Review generated plans and final reports before acting on them, especially for high-impact or customer-facing work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lingxinsuixing/principles-agent) <br>
- [Referenced principles project](https://github.com/miltonian/principles) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with structured task, validation, and integration results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a report only when the user provides an output path; LLM calls are supplied by the host environment.] <br>

## Skill Version(s): <br>
0.2.0 (source: evidence.release.version and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
