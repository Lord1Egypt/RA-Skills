## Description: <br>
Filter raw target lists into prioritized prospects worth pursuing by scoring fit, timing, value, and access, then routing each target to pursue, research, watch, or drop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[depinHQ](https://clawhub.ai/user/depinHQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, partnership, and business-development teams use Prospect before outreach to filter raw target lists, prioritize accounts, identify missing information, and choose whether to pursue, research, watch, or drop each target. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prospect evaluation may involve business-contact data, private relationship context, or sensitive attributes that are not needed for prioritization. <br>
Mitigation: Provide only the minimum target, company, role, and business signal data needed to score the prospect, and exclude information that cannot be used for marketing or outreach. <br>
Risk: Ambiguous requests could apply prospect scoring outside sales, partnerships, or business-development targeting. <br>
Mitigation: Confirm the request is for prospect evaluation in a sales, partnership, or business-development context before using the skill. <br>
Risk: Scores and routes can be misleading when source signals are sparse, stale, or uncertain. <br>
Mitigation: Treat missing information as an explicit gap, favor research or watchlist routes when evidence is weak, and apply human review before outreach. <br>


## Reference(s): <br>
- [Prospect on ClawHub](https://clawhub.ai/depinHQ/prospect) <br>
- [README](artifact/README.md) <br>
- [Examples](artifact/examples.md) <br>
- [Notes](artifact/notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown with prospect score breakdowns, route recommendations, summary tables for batches, and concise next steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scores prospects across fit, timing, value, and access, with total scores out of 40 and routes of pursue, research, watchlist, or drop.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
