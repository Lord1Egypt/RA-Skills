## Description: <br>
Self-Improvement Loop helps an agent mine weaknesses from execution traces, generate targeted improvements, validate their effect, and preserve lessons across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill after important tasks, failures, repeated mistakes, or scheduled review cycles to turn observed behavior into concrete, testable agent improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to keep cross-session records of failures, traces, mistakes, improvements, and validation history, which may capture sensitive task details. <br>
Mitigation: Use clear workspace boundaries, review generated traces for sensitive data, and avoid storing secrets or private user content in memory records. <br>
Risk: The skill can direct the agent to modify behavior files such as SKILL.md, MEMORY.md, or TOOLS.md, which can change future agent behavior. <br>
Mitigation: Require user confirmation and review before applying changes to core behavior files, and keep improvements small, targeted, testable, and reversible. <br>
Risk: Unvalidated self-improvements can degrade behavior or reinforce incorrect guidance. <br>
Mitigation: Run the documented proposal validation step, compare outcomes against the prior baseline, and roll back changes that regress quality or reliability. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON record templates with proposed file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update execution traces, weakness records, improvement proposals, validation records, metrics, and skill or memory files when permitted.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
