## Description: <br>
MetaClaw helps agents manage local memory through hybrid retrieval, memory extraction, session counting, and skill quality checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donmeusi](https://clawhub.ai/user/donmeusi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use MetaClaw to add an OpenClaw local-memory workflow that searches memory with semantic and keyword retrieval, extracts session facts into memory files, counts sessions for consolidation, and evaluates skill quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and update local OpenClaw memory files. <br>
Mitigation: Start with dry-run modes, keep the workspace scope intentional, and review file changes before relying on updated memory. <br>
Risk: Memory extraction can send session content to a local Ollama service. <br>
Mitigation: Confirm the local Ollama service is trusted before running extraction on sensitive session content. <br>
Risk: The quality auto-fix workflow can modify skill files when --allow-write is used. <br>
Mitigation: Use the preview mode first and review diffs before enabling --allow-write. <br>
Risk: Optional cron or heartbeat hooks can run memory maintenance without direct user initiation. <br>
Mitigation: Do not enable unattended hooks unless the user is comfortable with automatic memory maintenance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/donmeusi/metaclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON outputs from the included scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory files when the user runs the included scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
