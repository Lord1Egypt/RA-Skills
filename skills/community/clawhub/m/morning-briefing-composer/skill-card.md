## Description: <br>
Aggregates weather, game updates, and concert data into a daily markdown briefing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PatFitzner](https://clawhub.ai/user/PatFitzner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to compose a local daily briefing from configured weather, game update, and concert data sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured weather location is sent to wttr.in when weather is enabled. <br>
Mitigation: Review ~/.openclaw/config/morning-briefing.json before use and disable weather or change the location if that disclosure is not acceptable. <br>
Risk: Configured upstream data files and jq templates can influence markdown that is later presented verbatim to the user. <br>
Mitigation: Use trusted data files and templates, and review source configuration before relying on the generated briefing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PatFitzner/morning-briefing-composer) <br>
- [Publisher profile](https://clawhub.ai/user/PatFitzner) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown file with shell command output path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a composed briefing to artifact-local data/briefing.md and instructs the agent to present the generated markdown verbatim.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
