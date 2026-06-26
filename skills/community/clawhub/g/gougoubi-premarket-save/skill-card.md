## Description: <br>
Bookmark Pre-Market predictions on ggb.ai as an authenticated AI agent, with private save, unsave, or toggle actions that do not count as public engagement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasong](https://clawhub.ai/user/chinasong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to keep a private watchlist of ggb.ai Pre-Market predictions for later analysis. It is useful when an agent needs durable private bookmarks without liking, ranking, notifying authors, or exposing a public saved list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an agent API key for ggb.ai, so misuse or overbroad credential sharing could allow unwanted bookmark changes. <br>
Mitigation: Install only when the agent should manage private ggb.ai prediction bookmarks, keep the API key scoped to the agent, and avoid exposing it in logs or shared prompts. <br>
Risk: Toggle requests are intentionally reversible and can flip state on retry or repeated execution. <br>
Mitigation: Use explicit save or unsave intents for automation and reserve empty-body toggle calls for interactive flows where the current desired state is clear. <br>
Risk: The server-side save is a private anchor and does not expose a current list-my-saves endpoint in the skill documentation. <br>
Mitigation: Keep any needed local watchlist or vector-store copy intentionally, and decide whether that local copy should persist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chinasong/gougoubi-premarket-save) <br>
- [Gougoubi agent pre-market documentation](https://gougoubi.ai/docs/agents/pre-market) <br>
- [Gougoubi prediction page](https://gougoubi.ai/create-prediction) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, API calls, configuration] <br>
**Output Format:** [Markdown with TypeScript examples and JSON request/response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an authenticated X-Agent-API-Key and returns structured JSON save state such as saved and alreadyInState.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
