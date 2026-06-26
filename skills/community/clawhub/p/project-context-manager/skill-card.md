## Description: <br>
Project Context Manager helps agents maintain long-term project state across sessions through structured project notes, session traces, and safety-focused development routines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[changer-changer](https://clawhub.ai/user/changer-changer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and software engineering agents use this skill to keep structured project state across sessions, record task reasoning, and apply safety checks during multi-file development work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent project notes may capture secrets, personal data, or sensitive incident details. <br>
Mitigation: Review AI_DOC/PROJECT_CONTEXT.md, AI_DOC/AI_memory/, and AI_DOC/AI_FEEDBACK.md before committing or sharing, and avoid writing credentials or sensitive details into those files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update AI_DOC/PROJECT_CONTEXT.md, AI_DOC/AI_memory/, and AI_DOC/AI_FEEDBACK.md when applied by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
