## Description: <br>
Skill Hunter helps an agent search for reusable skills, tools, workflows, repositories, SDKs, APIs, and related resources before implementation, evaluate fit and risk, and ask for user approval before using external resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mturac](https://clawhub.ai/user/mturac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a pre-execution discovery step for coding, automation, data processing, deployment, and content tasks where an existing tool or workflow may save effort. It is intended to produce a recommendation and approval gate before external tools are installed, run, or granted access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation and vague routing boundaries can make the skill influence many unrelated development and content tasks. <br>
Mitigation: Enable it only when external tool discovery is desired, review its activation rules carefully, and keep explicit user approval before using external tools. <br>
Risk: Tool recommendations could steer users toward unsafe, incompatible, or overprivileged external resources. <br>
Mitigation: Review recommended tools for maintenance, permissions, credential scope, licensing, and security before installation or execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mturac/openclaw-skill-hunter) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown or plain text recommendations, shortlists, risk notes, and approval prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include candidate names, tool categories, fit rationale, risks, effort estimates, and a user approval question.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
