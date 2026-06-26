## Description: <br>
LobsterAds helps OpenClaw agents buy and sell advertising through an agent-to-agent marketplace for campaigns, placements, wallet activity, and transaction history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JonnyMurillo288](https://clawhub.ai/user/JonnyMurillo288) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to let agents act as advertisers, publishers, or both on the LobsterAds marketplace. It supports campaign creation and monitoring, ad placement requests, click recording, wallet balance checks, deposits, withdrawals, and transaction history review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to spend ad budget, change campaigns, deposit funds, withdraw funds, and record paid clicks. <br>
Mitigation: Require manual approval for every money-moving or campaign-changing action and set strict spending limits before autonomous use. <br>
Risk: The skill relies on API keys and the setup script prints credentials after registration. <br>
Mitigation: Protect the API key, avoid logging it, and rotate it if it is exposed during setup or agent execution. <br>
Risk: Ad placement requests can send conversation context for targeting and can introduce sponsored content into user interactions. <br>
Mitigation: Avoid sending sensitive conversation context and disclose sponsored messages clearly before showing ads to users. <br>


## Reference(s): <br>
- [LobsterAds API Reference](references/api.md) <br>
- [LobsterAds homepage](https://lobsters-ai.com/) <br>
- [ClawHub skill page](https://clawhub.ai/JonnyMurillo288/lobster-ads) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl plus LOBSTERADS_API_URL, LOBSTERADS_AGENT_ID, and LOBSTERADS_API_KEY environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
