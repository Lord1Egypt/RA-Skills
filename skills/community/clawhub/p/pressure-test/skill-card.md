## Description: <br>
Use when an idea, plan, design, or scope needs to be stress-tested before anyone builds it, when the user says "pressure test this", "poke holes in this", or wants the fuzzy parts made concrete. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[escoffier-labs](https://clawhub.ai/user/escoffier-labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and planning agents use this skill to pressure-test ideas, plans, designs, or implementation scope before build work begins. It helps turn vague proposals into explicit decisions, open questions, and a recommended next step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sous mode can make reversible planning calls on the user's behalf after handoff. <br>
Mitigation: Give clear instructions about which decisions the agent may make, require basis labels for each decision, and review the saved decision transcript before acting on it. <br>
Risk: A planning judgment could be mistaken for verified evidence. <br>
Mitigation: Preserve the skill's evidence, stated-constraint, and judgment labels so reviewers can distinguish inspected facts from agent judgment. <br>
Risk: The agent could drift into destructive, paid, public-facing, breaking, or otherwise hard-to-reverse decisions during autonomous planning. <br>
Mitigation: Park out-of-bounds decisions as open questions and choose only paths that keep those decisions reversible. <br>


## Reference(s): <br>
- [Pressure Test on ClawHub](https://clawhub.ai/escoffier-labs/pressure-test) <br>
- [Publisher profile: escoffier-labs](https://clawhub.ai/user/escoffier-labs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with concise decision records, open questions, and a recommended next step] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sous mode may include an auditable decision transcript with basis labels such as evidence, stated-constraint, and judgment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
