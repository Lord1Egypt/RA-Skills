## Description: <br>
HeyGen (heygen.com). Use this skill for ANY HeyGen request - reading, creating, updating, and deleting data. Whenever a task involves HeyGen, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate a connected HeyGen account through OOMOL for avatar and template video generation, status checks, quota/account reads, asset management, and video retrieval. It supports both read-only account inspection and state-changing HeyGen actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route broad HeyGen-related requests through a connected account. <br>
Mitigation: Install only when the agent should operate HeyGen, and review generated video requests before spending credits or using the output. <br>
Risk: Write actions can create videos or upload assets in the connected HeyGen account. <br>
Mitigation: Confirm the exact payload and intended account effect before running actions tagged as write operations. <br>
Risk: Destructive actions can delete HeyGen assets or videos. <br>
Mitigation: Require explicit user approval for the target asset or video before running destructive actions. <br>
Risk: The skill depends on a connected OOMOL account and HeyGen credentials. <br>
Mitigation: Use the connected-account flow described by the skill and avoid exposing or handling raw HeyGen API tokens. <br>


## Reference(s): <br>
- [HeyGen homepage](https://www.heygen.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-heygen) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector calls may return asynchronous job IDs, execution IDs, status data, download URLs, account data, quota data, asset IDs, or deletion results depending on the selected HeyGen action.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
