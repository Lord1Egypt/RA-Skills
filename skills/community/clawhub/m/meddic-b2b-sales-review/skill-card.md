## Description: <br>
Structured B2B sales review using the original PTC MEDDIC Six-Step methodology, with stage gates and win-rate calibration for opportunities, projects, pipelines, losses, coaching, and visit debriefs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales managers and frontline sales teams use this skill to review B2B opportunities, projects, pipelines, losses, one-on-one coaching, and customer visit debriefs. It helps evaluate MEDDIC evidence, validate sales-stage gates, calibrate forecast confidence, and produce concrete next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer visit debriefs can involve customer names, meeting notes, participants, follow-up dates, and other sensitive sales information. <br>
Mitigation: Before reading or appending customer notes, show what customer information will be used, request explicit confirmation, and avoid storing unnecessary personal or confidential details. <br>
Risk: Scheduled reminders can create ongoing outreach or monitoring if enabled without clear consent and scope. <br>
Mitigation: Enable reminders only after explicit opt-in, with clear frequency, date range, customer or opportunity scope, and a visible way to stop or revise the schedule. <br>
Risk: Sales-stage, forecast, and resource recommendations can be misleading when the input is incomplete or based mainly on seller impressions. <br>
Mitigation: Require the agent to call out missing evidence, separate customer-verified facts from assumptions, and keep management decisions subject to human review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/andyrenxu7255/meddic-b2b-sales-review) <br>
- [Publisher Profile](https://clawhub.ai/user/andyrenxu7255) <br>
- [Skill Index](SKILL.md) <br>
- [Opportunity Review](references/review-opportunity.md) <br>
- [Visit Debrief](references/review-visit.md) <br>
- [Six-Step Method](references/methods/six-step.md) <br>
- [MEDDIC Method](references/methods/meddic.md) <br>
- [Stage Gate Validation](references/scoring/stage-gate-validation.md) <br>
- [Output Format](references/templates/output-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown sales review summaries, MEDDIC gap diagnostics, stage and win-rate assessments, scorecards, action plans, follow-up templates, and reminder configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should distinguish verified evidence from assumptions, avoid unsupported optimistic judgments, and identify missing customer or opportunity information before recommending next actions.] <br>

## Skill Version(s): <br>
1.4.0 (source: evidence.release.version, SKILL.md frontmatter, clawhub.yaml, target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
