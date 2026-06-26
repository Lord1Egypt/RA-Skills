## Description: <br>
Guides an OpenClaw agent through Space-based social matching by introducing the product, onboarding a user, confirming a public profile, recommending a match, and handling opt-in platform messaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pikaqiu2333](https://clawhub.ai/user/pikaqiu2333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to join a Space, confirm a public profile, receive an initial social recommendation, choose follow-up recommendation and inbox polling preferences, and send platform messages only after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Space profile details, recommendations, and platform messages with api.clawspace.top. <br>
Mitigation: Install only if that sharing is acceptable, and submit public profile details only after explicit user confirmation. <br>
Risk: Operator-key troubleshooting access is broader than the normal user-facing matching workflow needs. <br>
Mitigation: Do not provide OPERATOR_API_KEY unless administrative troubleshooting access to spaces, members, or messages is intentionally required. <br>


## Reference(s): <br>
- [Skill homepage](https://pikaqiu2333.github.io/social-radar-skill/) <br>
- [ClawHub listing](https://clawhub.ai/pikaqiu2333/perfectmatch) <br>
- [ClawSpace API base](https://api.clawspace.top) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, API Calls, JSON] <br>
**Output Format:** [Markdown instructions with HTTP and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-facing onboarding, profile confirmation, recommendation, and messaging guidance for an OpenClaw agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
