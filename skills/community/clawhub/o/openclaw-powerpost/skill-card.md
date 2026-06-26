## Description: <br>
Generate social media content and publish to all major platforms from one command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tarekhoury](https://clawhub.ai/user/tarekhoury) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use Powerpost to have an agent draft, generate media for, schedule, publish, and analyze social media posts across connected accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, schedule, cancel, and delete content in connected social accounts. <br>
Mitigation: Use draft-only or narrowly scoped API keys by default, and require explicit user confirmation before live publishing or destructive calendar actions. <br>
Risk: The skill requires a PowerPost API key and workspace ID that grant access to workspace content and connected social accounts. <br>
Mitigation: Store credentials in the configured skill secret or environment paths, avoid displaying them, and prefer the least-privilege scopes needed for the task. <br>
Risk: Content, image, video, and publishing actions may spend PowerPost credits. <br>
Mitigation: Check the credit balance before generation or publishing and confirm credit-spending actions with the user. <br>


## Reference(s): <br>
- [PowerPost Homepage](https://powerpost.ai) <br>
- [PowerPost API Documentation](https://powerpost.ai/docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/tarekhoury/openclaw-powerpost) <br>
- [Publisher Profile](https://clawhub.ai/user/tarekhoury) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with curl commands and JSON request and response examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POWERPOST_API_KEY, POWERPOST_WORKSPACE_ID, and curl; can post externally and spend credits when authorized.] <br>

## Skill Version(s): <br>
0.4.0 (source: frontmatter, changelog, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
