## Description: <br>
Submit your project to Built at GrowthX, the community builder showcase for GrowthX members, using a GrowthX API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gxt-admin](https://clawhub.ai/user/gxt-admin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
GrowthX members and developers use this skill to detect project details from a workspace, confirm the final submission fields, and submit a project to Built at GrowthX. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A GrowthX API key could be exposed or reused outside the intended account context. <br>
Mitigation: Use a GrowthX-specific API key, store it in an environment variable or protected configuration, and do not share the key. <br>
Risk: Incorrect or unintended project details could be submitted to Built at GrowthX. <br>
Mitigation: Review the final project name, description, stack, URL, and status before approving submission. <br>
Risk: The skill sends project metadata to GrowthX. <br>
Mitigation: Install and use it only when you trust GrowthX and intend to submit project details there. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gxt-admin/growthx-bx-submit) <br>
- [Built at GrowthX Project Submission API](https://backend.growthx.club/api/v1/bx/projects/agent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON request fields and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before submission and uses GROWTHX_API_KEY for authentication.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
