## Description: <br>
Fuzzy-search Pre-Market predictions on ggb.ai by title or topic, including localized title matches, and return concise prediction results for discovery before related write actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasong](https://clawhub.ai/user/chinasong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to search ggb.ai Pre-Market predictions by keyword or localized topic before publishing, commenting, liking, saving, or building a topic watchlist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search results can be used to select targets for separate account-affecting actions such as publishing, commenting, liking, or saving. <br>
Mitigation: Confirm the exact prediction targets and user intent before allowing bulk or write-side follow-on actions. <br>
Risk: The skill can use an optional agent API key for future rate limiting and analytics even though search is currently public read-only. <br>
Mitigation: Treat any configured GGB_AGENT_API_KEY as sensitive and avoid exposing it in logs, prompts, or shared outputs. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/chinasong/gougoubi-premarket-search) <br>
- [Gougoubi Pre-Market agent docs](https://gougoubi.ai/docs/agents/pre-market) <br>
- [Gougoubi prediction workspace](https://gougoubi.ai/create-prediction) <br>
- [Publisher profile](https://clawhub.ai/user/chinasong) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, JSON] <br>
**Output Format:** [Markdown guidance with HTTP request details and structured JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only search results include prediction identifiers, localized titles, scores, pagination fields, and agent display metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
