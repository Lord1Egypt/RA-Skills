## Description: <br>
Build and run a behavior-first personal planning, triage, and decision agent that learns a user's values, goals, recurring problems, friction patterns, and decision standards over time, then gives strong recommendations for "what should I do now?", multi-problem triage, do-or-don't dilemmas, 3-6 month planning, weekly review, and proactive heartbeat follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lakendocean](https://clawhub.ai/user/lakendocean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals use this agent to turn personal goals, values, recurring problems, and real-world tradeoffs into clear priorities, decisions, plans, reviews, and follow-up commitments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive personal goals, values, decisions, behavior patterns, and follow-up commitments in durable workspace files. <br>
Mitigation: Review and prune generated files regularly, avoid storing highly sensitive journals or test results unless needed, and keep only information that improves future planning and judgment. <br>
Risk: The skill may produce strong personal planning or decision guidance that could be mistaken for professional medical, legal, financial, or mental-health advice. <br>
Mitigation: Use the guidance as personal planning support only, keep user agency explicit, and seek qualified professional advice for medical, legal, financial, or mental-health decisions. <br>
Risk: Proactive heartbeat follow-up can become intrusive if cadence, stop conditions, or escalation rules are unclear. <br>
Mitigation: Set clear heartbeat cadence, tone, escalation rules, and stop conditions before relying on recurring follow-up. <br>


## Reference(s): <br>
- [Bootstrap Questionnaire](references/bootstrap-questionnaire.md) <br>
- [File Contracts](references/file-contracts.md) <br>
- [Interaction Modes](references/interaction-modes.md) <br>
- [Judgment System](references/judgment-system.md) <br>
- [Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance and durable workspace file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update personal planning files such as USER.md, IDENTITY.md, GOALS.md, DECISION_RULES.md, DECISIONS.md, and HEARTBEAT.md.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
