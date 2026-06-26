## Description: <br>
Count tokens and estimate costs for 300+ LLM models, with a primary use case of auditing OpenClaw workspace token consumption across memory, persona, and skill files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zhaobudaoyuema](https://clawhub.ai/user/Zhaobudaoyuema) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to count prompt or file tokens, estimate model API costs, compare model token usage, and audit OpenClaw workspace context size before or after changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local OpenClaw workspace and skill files, which may contain personal data or secrets. <br>
Mitigation: Install and run it only when token auditing those files is intended, and avoid pointing it at sensitive files that are not needed for the audit. <br>
Risk: The URL input option can make outbound HTTP or HTTPS requests and may expose network metadata or interact with untrusted, localhost, or internal URLs. <br>
Mitigation: Use local files or inline text when possible, and require explicit user confirmation before fetching only trusted external URLs. <br>
Risk: The benchmark example can send text to a configured model API endpoint. <br>
Mitigation: Do not run API benchmarking on sensitive text unless the endpoint and credentials are trusted for that data. <br>


## Reference(s): <br>
- [Prompt Token Counter on ClawHub](https://clawhub.ai/Zhaobudaoyuema/prompt-token-counter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal-style text with token counts, cost estimates, model lists, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [OpenAI models use tiktoken when available; other model counts are approximate. Cost output depends on available pricing data.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
