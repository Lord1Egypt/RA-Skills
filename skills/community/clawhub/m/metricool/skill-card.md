## Description: <br>
Schedule and manage social media posts via Metricool API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[willscott-v2](https://clawhub.ai/user/willscott-v2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and social media teams use this skill to list Metricool brands, schedule posts across connected social platforms, inspect queued posts, and check suggested posting times. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can schedule public social posts on connected Metricool accounts using stored credentials. <br>
Mitigation: Use a dedicated or least-privilege Metricool token where available, keep credentials out of committed files, and confirm the post text, platforms, and scheduled time before running scheduling commands. <br>
Risk: Some scripts may use the first connected Metricool brand when a brand or blog ID is not provided. <br>
Mitigation: Supply the exact blogId or brand and target platforms for scheduling and review the selected brand before publishing. <br>


## Reference(s): <br>
- [Metricool](https://metricool.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/willscott-v2/metricool) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples; scripts can return text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Metricool credentials and connected brands before API-backed actions can run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
