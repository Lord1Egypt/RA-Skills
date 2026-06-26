## Description: <br>
Neta API research and recommendation skill for keyword, tag, and category suggestions, taxonomy path validation, and multi-mode content feeds that support exploration from broad topics to precise filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huxiuhan](https://clawhub.ai/user/huxiuhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to explore Neta content topics, discover related tags and categories, validate taxonomy paths, and retrieve recommendation, search, or exact-filter content feeds before creation or interaction workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs an external Neta CLI package and service. <br>
Mitigation: Install only when the publisher and Neta CLI package are trusted; prefer a pinned package version when possible. <br>
Risk: NETA_TOKEN is required and could be exposed through logs or shared prompts. <br>
Mitigation: Keep NETA_TOKEN out of logs and prompts, and use a minimally scoped token. <br>
Risk: Search terms, taxonomy filters, and recommendation requests may be sent to Neta. <br>
Mitigation: Avoid submitting sensitive topics or private filtering criteria unless the service is approved for that data. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/huxiuhan/neta-suggest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI command examples and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NETA_TOKEN and the Neta CLI; recommendation, search, taxonomy, and pagination inputs may be sent to the Neta service.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
