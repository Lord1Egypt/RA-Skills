## Description: <br>
Guides agents through a structured investment-analysis workflow for incremental updates from new materials, merging archived reports, and maintaining an investment stock pool while preserving continuity with prior archived analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcchris1995](https://clawhub.ai/user/pcchris1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to keep investment research notes consistent when reviewing new announcements, research reports, meeting notes, or archive reorganizations. It emphasizes reading existing archived reports first, mapping only incremental changes, and updating the appropriate investment files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide edits to investment archive notes and stock-pool records, so incorrect analysis or stale assumptions could be preserved in user files. <br>
Mitigation: Use explicit requests for updates, review diffs before accepting changes, and require source timestamps and reasons for each material change. <br>
Risk: Investment materials may contain private portfolio, account, or personal research details. <br>
Mitigation: Avoid processing private portfolio or account details unless necessary for the task, and limit shared context to the specific files needed for the requested update. <br>
Risk: Broad activation wording can make the workflow run for many investment-analysis prompts. <br>
Mitigation: Install only when an agent is expected to help maintain investment or financial archive notes, and confirm when the workflow should be applied. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pcchris1995/investment-analysis-workflow) <br>
- [Publisher profile](https://clawhub.ai/user/pcchris1995) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text, file updates] <br>
**Output Format:** [Markdown analysis, structured checklists, and proposed or applied archive updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve prior archived logic, cite material sources and timestamps, avoid target market-value predictions, and require user review before accepting changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
