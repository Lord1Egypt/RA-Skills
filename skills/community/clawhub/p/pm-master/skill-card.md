## Description: <br>
PM Master helps project managers coordinate BA and SA work across project kickoff, MVP planning, workload assessment, project planning, and iteration planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leo21cn](https://clawhub.ai/user/leo21cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Project managers and software delivery teams use this skill to draft project management artifacts, including iteration 0 plans, MVP plans, workload assessments, overall project plans, and detailed iteration plans. The skill's own guidance treats outputs as drafts that require review by a human PM before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route project requirements, architecture documents, estimates, and plans through a third-party remote MCP service. <br>
Mitigation: Install only when that service is trusted and approved for the project data being shared; avoid confidential or sensitive materials unless data handling terms are clear. <br>
Risk: The release embeds a reusable bearer token for the remote service. <br>
Mitigation: Rotate or replace the token before operational use and limit access to environments where the remote service is intended to be used. <br>
Risk: Generated schedules, estimates, and project plans may be incomplete or incorrect. <br>
Mitigation: Treat outputs as drafts and require review by a human project manager before using them for commitments or delivery decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leo21cn/pm-master) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown documents and conversational text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PM planning drafts, estimates, risk notes, and staged prompts that require human review before adoption.] <br>

## Skill Version(s): <br>
1.5.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
