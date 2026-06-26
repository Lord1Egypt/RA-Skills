## Description: <br>
会话日志分析 - 搜索和分析历史会话日志，查找之前的对话内容和结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect recent OpenClaw session logs, search for keywords, and summarize relevant historical prompts, commands, and results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local session logs may contain private prompts, commands, secrets, or customer data. <br>
Mitigation: Limit searches to the needed time range and review returned snippets before sharing or storing them. <br>
Risk: Search results can expose sensitive context from previous agent sessions. <br>
Mitigation: Redact sensitive values and avoid broad keyword searches on logs that may contain confidential information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-session-logs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown summaries with optional Python code examples and log-result snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include local session filenames, timestamps, line numbers, and truncated log excerpts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
