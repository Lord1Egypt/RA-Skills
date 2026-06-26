## Description: <br>
meeting-score helps meeting hosts create Feishu Bitable agenda scoring tables, collect independent H/M/L judge scores, and summarize average scores by agenda. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lixiaojie-1012](https://clawhub.ai/user/lixiaojie-1012) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Meeting hosts and facilitators use this skill to set up Feishu Bitable scoring sheets for agenda items, guide judges through independent scoring, and generate ranked score summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and modify Feishu Bitable scoring data, including cleanup and score updates. <br>
Mitigation: Confirm the target table and record identifiers before cleanup or updates, and review generated scoring tables before sharing them. <br>
Risk: Judges may see other judges' scoring rows if Feishu row-level permissions are not configured correctly. <br>
Mitigation: Configure and verify advanced row-level permissions before inviting judges to use the scoring table. <br>
Risk: Automatic polling can continue after scoring is complete. <br>
Mitigation: Stop the scheduled polling job when scoring is finished or no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lixiaojie-1012/meeting-score) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions, confirmations, and score summary tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Feishu Bitable tables and scheduled polling jobs when the required tools are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
