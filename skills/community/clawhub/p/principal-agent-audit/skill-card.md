## Description: <br>
Audit a principal AI agent or coordinator bot: review memory, learnings, recent errors, installed skills, operational risks, delegation posture, and propose controlled improvements without autonomous self-modification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juanbastias](https://clawhub.ai/user/juanbastias) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit a main AI assistant or coordinator agent that has access to user context, tools, memory, and other agents. It helps review reliability, privacy, coordination, memory hygiene, tooling posture, and operational risks before proposing controlled improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may review sensitive local agent context such as memory, notes, learnings, installed skills, and scheduled-work context. <br>
Mitigation: Use it only for intended local audits, summarize sensitive patterns instead of quoting secrets or full private logs, and gather only the smallest useful context. <br>
Risk: Implicit invocation can trigger the audit helper when prompts are ambiguous. <br>
Mitigation: Use clear audit prompts and require explicit approval before edits, scheduler changes, authentication changes, publishing, package installation, or network lookup. <br>
Risk: Audit recommendations could lead to unsafe self-modification or changes to principal-agent behavior if applied automatically. <br>
Mitigation: Treat findings as proposals first, prefer reversible edits with written rationale, and avoid auto-modifying personality, memory policy, routing policy, delegation rules, or coordination behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juanbastias/principal-agent-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown operator briefing with verdict, evidence, risk, recommendation, and next action] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May list exact files touched when changes are explicitly requested.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
