## Description: <br>
Search and analyze your own session logs (older/parent conversations) using jq. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to locate, filter, and summarize prior OpenClaw session JSONL logs when a user asks about older or parent conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive content from prior local conversation logs. <br>
Mitigation: Use it only for explicit recovery tasks, narrow searches by date, topic, or session, and ask the agent to summarize or redact sensitive matches. <br>
Risk: Broad keyword searches may return more historical context than the user intended to share. <br>
Mitigation: Start with constrained queries and inspect small samples before extracting full message text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/huimai-session-logs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local jq and rg binaries and access to the user's local OpenClaw session log directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
