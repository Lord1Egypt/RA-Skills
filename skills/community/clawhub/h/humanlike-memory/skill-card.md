## Description: <br>
HumanLike Memory / Human-Like Memory is a persistent AI agent memory system for long-term memory search, recall, and save. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[humanlike2026](https://clawhub.ai/user/humanlike2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to let an agent explicitly search, recall, and save long-term memory when prior context, user preferences, decisions, or reusable procedures are relevant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recall and save commands send queries, message content, user identifiers, and agent identifiers to a configured remote memory service. <br>
Mitigation: Use the skill only with a trusted endpoint, review the service privacy policy, and avoid saving secrets, tokens, private command output, or sensitive tool results. <br>
Risk: The skill requires a sensitive API key for the remote memory service. <br>
Mitigation: Store the API key through OpenClaw configuration or explicit environment injection; do not hard-code it in prompts, scripts, or shared files. <br>
Risk: Optional auto-save and tool-call capture can preserve more conversation or tool-result context than intended. <br>
Mitigation: Disable HUMAN_LIKE_MEM_AUTO_SAVE_ENABLED or HUMAN_LIKE_MEM_CAPTURE_TOOL_CALLS unless those behaviors are explicitly needed, and prefer explicit saves for sensitive workflows. <br>


## Reference(s): <br>
- [Human-Like Memory Service](https://plugin.human-like.me) <br>
- [ClawHub Skill Page](https://clawhub.ai/humanlike2026/humanlike-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and JSON from Node.js CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include recalled memory snippets, save confirmations, and configuration status; remote requests require HUMAN_LIKE_MEM_API_KEY.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
