## Description: <br>
Openclaw Memory Stack provides an OpenClaw memory plugin with local multi-engine search, structured fact extraction, deduplication, cross-agent sharing, and self-healing maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apptah](https://clawhub.ai/user/apptah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to give OpenClaw agents persistent local memory, routed search, fact recall, and token-controlled context reuse across projects and agent clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically capture conversation memory and alter OpenClaw memory-provider configuration. <br>
Mitigation: Review the installer and configuration changes before deployment, and use it only where automatic memory capture and provider takeover are acceptable. <br>
Risk: Fact extraction can send conversation excerpts to a user-configured or OpenAI cloud endpoint when API keys are configured. <br>
Mitigation: Remove OPENAI_API_KEY and OPENCLAW_LLM_API_KEY or configure a local-only endpoint when sensitive content should remain on the machine. <br>
Risk: The skill performs local command execution for memory storage and search dependencies. <br>
Mitigation: Deploy only where bounded local execution of sqlite3, qmd, and dependency bootstrapping is acceptable. <br>


## Reference(s): <br>
- [Openclaw Memory Stack ClawHub Release](https://clawhub.ai/apptah/openclaw-memory-stack) <br>
- [Openclaw Memory Stack GitHub Repository](https://github.com/Apptah/openclaw-memory-stack) <br>
- [Bun Runtime](https://bun.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return tiered memory context from compact summaries to full recalled content.] <br>

## Skill Version(s): <br>
0.6.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
