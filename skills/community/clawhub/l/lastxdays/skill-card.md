## Description: <br>
Research and summarize what happened in the last N days or a date range about a topic, optionally using Reddit API and X ingestion via x-cli, API, or local archive with graceful fallback to web. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[levineam](https://clawhub.ai/user/levineam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to gather recent web, Reddit, and X activity about a topic and produce a concise Markdown briefing with themes, notable links, and follow-up searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Reddit or X ingestion can use local credentials, x-cli configuration, API tokens, or a local X archive. <br>
Mitigation: Use web-only mode by default; enable Reddit or X only after confirming the helper scripts, credential sources, and local data access are intended. <br>
Risk: The skill can run local helper commands that are not bundled in the artifact evidence. <br>
Mitigation: Review any referenced local scripts before execution and prefer the documented web fallback when the scripts are absent or untrusted. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown briefing with links, bullets, and copy/pasteable follow-up searches] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source-grouped notable links for web, Reddit, and X; helper commands are optional and fall back to web search when credentials or local data are unavailable.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
