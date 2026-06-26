## Description: <br>
Dynamic, Grok 4.3-inspired analyzer for X (Twitter) posts, threads, trends, user activity, and related data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igorganapolsky](https://clawhub.ai/user/igorganapolsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to fetch, summarize, and inspect X/Twitter posts, threads, trends, replies, and engagement signals from user-provided X content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may fetch X/web content, including through an authenticated xurl setup, and can expose external content to the agent. <br>
Mitigation: Require explicit user confirmation before fetching external content and avoid accessing local xurl credentials directly. <br>
Risk: The security review notes broad, hidden activation and subagent delegation that users may not notice. <br>
Mitigation: Make activation and any subagent delegation visible to the user before deep analysis begins. <br>
Risk: The included helper script can fall back to mock data, which may produce inaccurate analysis if treated as real results. <br>
Mitigation: Clearly label fallback data as mock output or repair the helper before relying on it for accurate results. <br>


## Reference(s): <br>
- [xurl CLI reference](references/xurl.md) <br>
- [ClawHub skill page](https://clawhub.ai/igorganapolsky/grok-x-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown analysis with optional JSON from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch live X/web content through xurl or web tools and may delegate deeper analysis to subagents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
