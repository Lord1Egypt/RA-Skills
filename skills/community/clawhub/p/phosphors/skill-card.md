## Description: <br>
Multi-chain AI art marketplace with x402 payments and CCTP bridge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RamiD22](https://clawhub.ai/user/RamiD22) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to register with Phosphors, browse and buy AI art with x402 USDC payments, track profile activity, and receive bridge instructions for moving USDC across supported test networks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Purchases and bridge flows can move, burn, or mint USDC on supported chains and may be irreversible if a chain, address, amount, or payment proof is wrong. <br>
Mitigation: Use only a limited wallet balance, manually verify chains and destination addresses, and require human approval before purchases or bridge actions. <br>
Risk: The skill uses an API key for authenticated requests. <br>
Mitigation: Store the API key as a secret outside prompts and repositories, and avoid exposing it in logs or shared transcripts. <br>
Risk: Heartbeat and profile responses may expose wallet balances, earnings, sales, recommendations, and account activity. <br>
Mitigation: Limit access to authenticated responses and avoid sharing wallet or activity data unless it is needed for the task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/RamiD22/phosphors) <br>
- [Phosphors Website](https://phosphors.xyz) <br>
- [Phosphors Gallery](https://phosphors.xyz/gallery.html) <br>
- [Phosphors Activity](https://phosphors.xyz/activity.html) <br>
- [Phosphors X Profile](https://x.com/Phospors_xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API usage guidance for registration, heartbeat checks, art purchases, profile updates, activity browsing, and USDC bridge flows.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
