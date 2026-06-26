## Description: <br>
Fetch and track OpenRouter AI model rankings, including weekly trends, top models, top apps, and market share. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yufeinever](https://clawhub.ai/user/yufeinever) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and analysts use this skill to fetch OpenRouter ranking data, review weekly AI model usage trends, and generate recurring reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved ranking data may remain on the local machine under ~/.openclaw/data/openrouter-rankings when --save is used. <br>
Mitigation: Use --save only when local retention is intended, and delete saved files when they are no longer needed. <br>
Risk: Using --push may send ranking data to Feishu. <br>
Mitigation: Review Feishu credentials and destination settings before enabling --push. <br>


## Reference(s): <br>
- [OpenRouter Rankings](https://openrouter.ai/rankings) <br>
- [ClawHub Skill Page](https://clawhub.ai/yufeinever/openrouter-rankings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Markdown report with optional JSON and Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional --save writes ranking data under ~/.openclaw/data/openrouter-rankings; optional --json prints structured JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
