## Description: <br>
Learn-X is a subject-agnostic Socratic coaching skill that helps users learn a topic through diagnosis, single-concept pacing, structured questions, and learner-produced artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dimayip](https://clawhub.ai/user/dimayip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners and coaching agents use this skill to turn requests such as "teach me X" or "help me understand Y" into guided learning sessions. It is designed for programming, math, design patterns, tools, frameworks, domain knowledge, and soft skills where the learner should actively reason and leave with a concrete artifact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be a poor fit for users who need direct answers rather than Socratic coaching. <br>
Mitigation: Route only learning-oriented requests to this skill and allow the host agent to bypass it for direct-answer workflows. <br>
Risk: The skill is not intended as specialized medical, legal, financial, or debugging guidance. <br>
Mitigation: Use host-agent routing and policy checks to send those requests to appropriate domain-specific workflows. <br>
Risk: The skill source is primarily Chinese and may not fit English-only deployments without host-agent language handling. <br>
Mitigation: Confirm language expectations during deployment and route or adapt English-only sessions before enabling broadly. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dimayip/learn-x) <br>
- [Diagnosis playbook](references/diagnose-playbook.md) <br>
- [Question templates](references/question-templates.md) <br>
- [Session patterns](references/session-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown conversation guidance with structured choices, short prompts, milestone plans, microtasks, and learner artifact options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No hidden execution, data access, or destructive behavior is reported by the security evidence.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
