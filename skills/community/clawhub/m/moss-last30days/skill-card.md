## Description: <br>
Researches recent Reddit, X, and web discussions on a topic, synthesizes current findings, and helps produce copy-paste-ready prompts or recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangwzh](https://clawhub.ai/user/jiangwzh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to research what people have discussed, recommended, or announced about a topic during the last 30 days, then synthesize those findings into actionable summaries and prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics may be sent to OpenAI, xAI, Reddit, and web search providers when the corresponding modes are used. <br>
Mitigation: Avoid sensitive private topics and install only when external-service use is acceptable. <br>
Risk: API keys, cached results, and raw research outputs may be stored locally. <br>
Mitigation: Prefer environment variables or a secret manager for keys, and periodically review or delete ~/.config/last30days/.env, ~/.cache/last30days, and ~/.local/share/last30days/out. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiangwzh/moss-last30days) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with optional shell command blocks, configuration guidance, source statistics, and copy-paste prompt text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include Reddit and X engagement metrics when API keys are configured, or web-only findings when they are not.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
