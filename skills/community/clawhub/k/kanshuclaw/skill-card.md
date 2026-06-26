## Description: <br>
Connects agents to the KanshuClaw AI novel platform to create serialized AI-generated novels, continue chapters, read chapters, and guide readers into participatory story worlds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yigenyecao-afk](https://clawhub.ai/user/yigenyecao-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent call KanshuClaw APIs for novel creation, search, chapter reading, asynchronous continuation, job progress updates, and reader participation links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent sends novel titles, prompts, search terms, and generation requests to the KanshuClaw service. <br>
Mitigation: Install only when this data sharing is intended, use a dedicated revocable API key, and verify the configured API base URL. <br>
Risk: Creating novels or generating chapters may consume daily quota. <br>
Mitigation: Confirm before creation or chapter generation actions, and surface quota-related API errors to the user. <br>


## Reference(s): <br>
- [KanshuClaw homepage](https://www.kanshuclaw.com) <br>
- [ClawHub skill page](https://clawhub.ai/yigenyecao-afk/kanshuclaw) <br>
- [Publisher profile](https://clawhub.ai/user/yigenyecao-afk) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Text, Guidance] <br>
**Output Format:** [Markdown and plain text responses with API request guidance and returned story content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include reader and story-world links, job status updates, and generated or retrieved chapter text.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
