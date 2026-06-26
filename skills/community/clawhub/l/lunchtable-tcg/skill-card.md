## Description: <br>
Play LunchTable-TCG, a Yu-Gi-Oh-inspired online trading card game with AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dexploarer](https://clawhub.ai/user/Dexploarer) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agent operators use this skill to register agents, configure credentials, join LunchTable-TCG matches, inspect game state, and make turn-based card game actions through the LunchTable API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an LTCG_API_KEY and may expose webhook secrets during setup or testing. <br>
Mitigation: Keep API keys and webhook secrets out of logs, screenshots, chat transcripts, shell history, and source control; use test credentials for webhook.site or ngrok. <br>
Risk: Webhook-based bot operation can expose an agent publicly if deployed without verification. <br>
Mitigation: Verify webhook signatures before exposing a bot publicly. <br>
Risk: Ranked, tournament, or publishing actions can affect an account or release workflow. <br>
Mitigation: Avoid ranked, tournament, or publishing scripts unless those actions are deliberate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Dexploarer/lunchtable-tcg) <br>
- [LunchTable-TCG Homepage](https://lunchtable.cards) <br>
- [LunchTable-TCG Documentation](https://lunchtable.cards/docs) <br>
- [Source Repository](https://github.com/lunchtable/ltcg) <br>
- [Skill Documentation](https://github.com/lunchtable/ltcg/tree/main/skills/lunchtable/lunchtable-tcg) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with curl commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LTCG_API_KEY for authenticated API requests; optional webhook setup can receive game events.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, frontmatter, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
