## Description: <br>
MyReels API helps agents generate images, videos, speech, or music with MyReels, inspect live model schemas, submit generation tasks, list authenticated tasks, and poll task status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beautyaiclub](https://clawhub.ai/user/beautyaiclub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to integrate with MyReels generation workflows, choose models from live API metadata, submit media generation tasks, and retrieve generated result URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a MyReels access token and can submit generation tasks against the configured API endpoint. <br>
Mitigation: Use a dedicated revocable access token, keep ~/.myreels/config private with restrictive permissions, and confirm MYREELS_BASE_URL points to the official or trusted endpoint before use. <br>
Risk: Generation tasks can consume MyReels points or subscription quota. <br>
Mitigation: Review the live model metadata and estimatedCost before submitting generation requests. <br>
Risk: Task polling can hit query limits if repeated too quickly. <br>
Mitigation: Follow the documented polling intervals and back off if the API returns rate-limit responses. <br>


## Reference(s): <br>
- [MyReels homepage](https://myreels.ai) <br>
- [MyReels developer portal](https://myreels.ai/developer) <br>
- [ClawHub release page](https://clawhub.ai/beautyaiclub/myreels-api) <br>
- [Live Model Metadata](references/models.md) <br>
- [Code Examples](references/code-examples.md) <br>
- [Error Handling](references/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON API payloads, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return task IDs, polling guidance, status summaries, and result URLs from MyReels API responses.] <br>

## Skill Version(s): <br>
1.0.9 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
