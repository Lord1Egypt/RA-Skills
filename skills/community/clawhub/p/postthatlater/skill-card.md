## Description: <br>
Schedule and manage social media posts across multiple social platforms, query analytics, manage the queue, and publish immediately through natural language using the PostThatLater API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[col000r](https://clawhub.ai/user/col000r) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent schedule, update, delete, immediately publish, and analyze social media posts through PostThatLater. It is intended for connected social accounts authorized by the user's PostThatLater API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates on connected social media accounts using a PostThatLater API key. <br>
Mitigation: Install only when the publisher and service are trusted, treat PTL_API_KEY like a password, and avoid exposing it in logs or shared shell profiles. <br>
Risk: Scheduling, deleting, updating, or immediately publishing posts can change public social media content, and immediate publishing is irreversible. <br>
Mitigation: Have the agent ask for explicit user confirmation before scheduling, deleting, updating, or publishing posts, and verify account IDs, platform limits, and timezone conversions first. <br>


## Reference(s): <br>
- [PostThatLater homepage](https://postthatlater.com) <br>
- [ClawHub PostThatLater listing](https://clawhub.ai/col000r/postthatlater) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PTL_API_KEY and user confirmation before scheduling, deleting, updating, or immediately publishing posts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
