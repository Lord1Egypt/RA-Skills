## Description: <br>
OPC Board stress-tests one-person company, side project, solo venture, and open-source project ideas with five advisors across logic, deliverability, growth, viability, and risk, then outputs a scored feasibility report with a Go/No-Go decision. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris1wang3](https://clawhub.ai/user/chris1wang3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, indie founders, developers, creators, consultants, and open-source maintainers use this skill to evaluate whether a solo idea is viable before committing time or resources. It guides the agent through intake, five-advisor challenge, deterministic scoring, and a decision-oriented feasibility report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill steers matching idea-feasibility requests into a structured report that appears to be primarily Chinese, which may not fit every deployment audience. <br>
Mitigation: Review trigger wording, report language, and templates before use; adapt them for the intended users and locale. <br>
Risk: Sparse user input can make feasibility scores misleading. <br>
Mitigation: Preserve the intake checklist, missing-information labels, conservative scoring for skipped items, and failure path when there is not enough evidence to judge any dimension. <br>
Risk: The skill may discuss legal, financial, medical, or compliance-sensitive ideas only as risk prompts, not as professional advice. <br>
Mitigation: Keep the disclaimer and route regulated-domain conclusions to qualified review instead of treating the report as a compliance plan. <br>


## Reference(s): <br>
- [OPC scoring engine](references/scoring-engine-deterministic.md) <br>
- [Markdown report template](references/report-template-markdown.md) <br>
- [Professional HTML report template](references/report-template-pro.html) <br>
- [Five advisor guidance](references/soul.md) <br>
- [ClawHub release page](https://clawhub.ai/chris1wang3/opc-board) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown report by default, with an optional HTML report template and structured scoring guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes an intake checklist, 25-item scoring table, Go/Conditional/No Go decision, OPC decision card, pre-mortem, MoSCoW scope, action list, and disclaimer.] <br>

## Skill Version(s): <br>
1.3.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
