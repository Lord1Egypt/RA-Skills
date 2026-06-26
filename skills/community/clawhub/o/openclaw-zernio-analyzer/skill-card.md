## Description: <br>
Analyzes Zernio.com profiles, posts, companies, jobs, and trends to extract structures, networks, engagement, and career insights from URLs and content requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igorganapolsky](https://clawhub.ai/user/igorganapolsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to recognize Zernio-related requests, fetch public Zernio profile, job, company, and post information, and produce concise structure, network, engagement, and career insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports hidden activation and opaque fetching of public Zernio profile and engagement data. <br>
Mitigation: Use only for explicit user-requested Zernio targets, disclose when external web requests occur, and ask before broad profile, engagement, or network analysis. <br>
Risk: Fetched public profile, job, company, or post information may be incomplete, stale, or sensitive in context. <br>
Mitigation: Limit analysis to public data and user-provided targets, verify important claims against the source page, and avoid unsupported personal or career conclusions. <br>
Risk: Deep-dive behavior can expand the scope of analysis beyond the user's immediate request. <br>
Mitigation: Require explicit approval and a narrow target scope before spawning subagents or conducting broader job, network, or engagement analysis. <br>


## Reference(s): <br>
- [Zernio patterns reference](references/zernio_patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON-style analysis with optional command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concise profile, network, engagement, and career insights for user-requested Zernio targets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
