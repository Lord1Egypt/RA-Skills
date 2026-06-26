## Description: <br>
Calculate PI/PID controller gains using Internal Model Control (IMC) tuning rules for first-order systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and control engineers use this skill to derive IMC-based PI/PID gains for first-order process models and to reason about the lambda trade-off between response speed and robustness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Controller gains or sample controller logic could be unsafe if applied directly to HVAC, industrial, or other physical equipment. <br>
Mitigation: Validate in simulation first, apply output limits and anti-windup, add input validation, fault handling, and manual override, then perform supervised staged testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/hvac-control-imc-tuning-rules) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code] <br>
**Output Format:** [Markdown with formulas and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides reference controller-tuning guidance; users must validate gains for their target equipment and operating limits.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
