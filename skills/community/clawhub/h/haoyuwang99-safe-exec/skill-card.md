## Description: <br>
Analyze the intent of any script or code before executing it, to detect malicious, suspicious, or unintended behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haoyuwang99](https://clawhub.ai/user/haoyuwang99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill before running scripts from emails, external users, user-provided files, unknown skills, or other untrusted sources. It guides the agent to read the full code, reason through behavior, flag suspicious patterns, and return a run, review, or block recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Intent analysis can miss novel or indirect malicious behavior when code is obfuscated or behavior is hidden across code paths. <br>
Mitigation: Read the full script, trace every path, flag obfuscation and hidden side effects, and block execution when the behavior remains unclear. <br>
Risk: The skill may cause an agent to pause before executing unfamiliar scripts. <br>
Mitigation: Use the pause as a conservative review step for untrusted code and proceed only after the findings support the requested execution. <br>


## Reference(s): <br>
- [Safe Exec on ClawHub](https://clawhub.ai/haoyuwang99/haoyuwang99-safe-exec) <br>
- [haoyuwang99 publisher profile](https://clawhub.ai/user/haoyuwang99) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown intent analysis with verdict, summary, findings, and recommendation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code is bundled; the skill produces review guidance before an agent runs untrusted scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
