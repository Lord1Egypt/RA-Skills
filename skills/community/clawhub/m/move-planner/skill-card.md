## Description: <br>
Use this skill when a user is actively planning, in the middle of, or wrapping up a residential move. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris-openclaw](https://clawhub.ai/user/chris-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users planning a residential move use this skill to organize move timelines, tasks, vendors, address changes, budgets, and buy/sell milestones in a local tracker. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local move tracker can contain addresses, household notes, vendor contacts, and budget items. <br>
Mitigation: Keep move-data.json in a trusted local workspace and do not enter SSNs, full account numbers, full ID numbers, passport numbers, or mortgage application documents. <br>
Risk: Printable timelines, vendor lists, or move-day plans may expose personal move details if shared without review. <br>
Mitigation: Review generated exports before sharing them and remove details that third parties do not need. <br>


## Reference(s): <br>
- [Move Planner ClawHub Page](https://clawhub.ai/chris-openclaw/move-planner) <br>
- [README](artifact/README.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or plain text responses, with local JSON tracker updates when the agent is allowed to write files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local move-data.json file for move details, task progress, vendors, address changes, budget items, and milestone tracking.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter, changelog, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
