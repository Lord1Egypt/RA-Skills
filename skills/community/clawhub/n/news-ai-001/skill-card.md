## Description: <br>
Delivers a daily news digest to a Discord channel via webhook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ScottLL](https://clawhub.ai/user/ScottLL) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to gather recent AI and technology news, format a short daily digest, and post it to a configured Discord channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Discord webhook URL grants posting access to the target channel if exposed. <br>
Mitigation: Use a dedicated webhook for this skill and keep the webhook URL private. <br>
Risk: News summaries or selected links may be incorrect, stale, duplicated, or inappropriate for important channels. <br>
Mitigation: Preview the digest before posting to important channels and verify sources for time-sensitive or high-impact items. <br>
Risk: The artifact describes scheduled delivery but does not include a scheduler. <br>
Mitigation: Configure and verify any external scheduler separately before relying on recurring delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ScottLL/news-ai-001) <br>
- [Publisher profile](https://clawhub.ai/user/ScottLL) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON story objects and shell commands; the bundled script posts a Discord embed payload.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses up to five stories with headline, summary, and URL fields; requires a Discord webhook URL at runtime.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
