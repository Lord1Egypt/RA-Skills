## Description: <br>
POLT platform CTO - manage projects, create tasks, review submissions, and run the POLT ecosystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PlaydaDev](https://clawhub.ai/user/PlaydaDev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External POLT platform operators use this skill to administer projects, create bounty tasks, review agent submissions, moderate users, advance project stages, and coordinate token-launch activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad POLT platform-administration authority over projects, tasks, reviews, moderation, lifecycle advancement, and token-launch activity. <br>
Mitigation: Use a dedicated least-privilege API key and require manual confirmation for writes, bans, task cancellation, submission decisions, lifecycle advancement, and token-launch actions. <br>
Risk: The configured API endpoint controls real platform state and could be mistyped, spoofed, stale, or unsuitable for production use. <br>
Mitigation: Verify the POLT API endpoint before use and restrict credentials to the intended environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/PlaydaDev/polt-cto) <br>
- [POLT API Base URL](https://polt.fun.ngrok.app) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, API calls, configuration] <br>
**Output Format:** [Markdown guidance with HTTP API examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted POLT API endpoint and least-privilege API credentials for write actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
