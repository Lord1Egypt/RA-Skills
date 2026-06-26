## Description: <br>
PaperDaily recommends high-value recent computer science papers from arXiv. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xyc5872](https://clawhub.ai/user/xyc5872) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical teams use PaperDaily to fetch daily or refreshed arXiv computer science paper recommendations in chat. It scores recent papers using recency, keyword matches, and information density. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates its main runtime behavior to the external openclaw-paperdaily npm package, whose permission bounds are not clear from the artifact. <br>
Mitigation: Review the dependency before installing and pin an exact version where possible. <br>
Risk: Feishu app credentials and chat access could expose broader tenant or chat permissions if over-scoped. <br>
Mitigation: Use a dedicated least-privilege Feishu app limited to the target chat, avoid reusing broad credentials, and rotate the secret if dependency or permission concerns arise. <br>


## Reference(s): <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [PaperDaily on ClawHub](https://clawhub.ai/xyc5872/paperdaily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration guidance] <br>
**Output Format:** [Chat response with paper recommendations; setup guidance uses environment-variable configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses cached daily results unless a refresh command is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
