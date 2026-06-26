## Description: <br>
Uses the RollingGo CLI to search hotels, filter results, read hotel tags, and retrieve hotel details, room prices, and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longcreat](https://clawhub.ai/user/longcreat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find hotel candidates by destination, dates, budget, star rating, tags, or distance, then compare structured results and retrieve room details and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the RollingGo package and hotel API provider. <br>
Mitigation: Install only if the package and API provider are trusted, and use the documented npm/npx or uv/uvx execution path for the user's environment. <br>
Risk: Hotel searches can include sensitive travel details and an API key. <br>
Mitigation: Prefer AIGOHOTEL_API_KEY over passing keys with --api-key, avoid sharing logs or screenshots that contain secrets, and keep searches user-directed when sending dates, locations, budgets, or occupancy details. <br>


## Reference(s): <br>
- [RollingGo CLI Homepage](https://mcp.agentichotel.cn) <br>
- [RollingGo API Key Application](https://mcp.agentichotel.cn/apply) <br>
- [RollingGo NPX Reference](references/rollinggo-npx.md) <br>
- [RollingGo UV Reference](references/rollinggo-uv.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/longcreat/hotel-recommendation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON-oriented CLI output handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RollingGo CLI and AIGOHOTEL_API_KEY; default CLI stdout is JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
