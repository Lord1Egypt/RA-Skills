## Description: <br>
Project Review Council is a Chinese-first workflow for multi-role project audits, post-mortems, business evaluations, risk reviews, red-team reviews, and Go/No-Go decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qomob](https://clawhub.ai/user/qomob) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, founders, product leaders, investors, and operators use this skill to run a structured project review council that examines strategy, technology, product, security, growth, finance, competition, and execution risk. It produces evidence-tagged findings, role reports, risk rankings, scoring, and a final decision memo. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive business or project material may be included in the review context. <br>
Mitigation: Only provide project documents you are comfortable having analyzed by the agent. <br>
Risk: Chinese-first defaults may not match non-Chinese teams or review audiences. <br>
Mitigation: Confirm the desired output language before starting the review. <br>
Risk: Incomplete project evidence can lead to weak or unverifiable conclusions. <br>
Mitigation: Use the workflow checkpoints and evidence tags to identify missing material before relying on the final decision memo. <br>


## Reference(s): <br>
- [Source repository (server-resolved provenance)](https://github.com/qomob/project-review-council) <br>
- [ClawHub skill page](https://clawhub.ai/qomob/skills/project-review-council) <br>
- [Decision matrix](rubrics/decision-matrix.md) <br>
- [Scoring rubric](rubrics/scoring.md) <br>
- [Final decision workflow](workflows/09-decision.md) <br>
- [Red-blue review workflow](workflows/10-red-blue.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reports, scorecards, risk tables, role reports, and final decision memos] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-first output by default; strict evidence tags are required for conclusions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
