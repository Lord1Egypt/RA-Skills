## Description: <br>
Filesystem message bus and webhook relay for multi-agent IDE coordination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ThinkOffApp](https://clawhub.ai/user/ThinkOffApp) <br>

### License/Terms of Use: <br>
AGPL-3.0-only <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate IDE-based agents through local queues, webhook relay, room polling, scheduled jobs, and controlled shell-command workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional networking can send data to external URLs or receive local webhooks when configured. <br>
Mitigation: Keep default local-only settings unless networking is needed, keep the relay bound to localhost where appropriate, and review every URL used with emit or hooks create. <br>
Risk: Advanced commands may require credentials such as OpenClaw tokens, Ant Farm API keys, or webhook secrets. <br>
Mitigation: Leave credential fields empty until required, scope credentials narrowly, and avoid committing or broadly sharing ide-agent-kit.json. <br>
Risk: tmux run and exec can execute shell commands if the allowlist is too broad. <br>
Mitigation: Keep tmux.allow limited to trusted commands and use the exec approval flow before running requested commands. <br>
Risk: Persistent queues, receipts, memory files, sessions, and scheduled jobs may retain sensitive coordination data. <br>
Mitigation: Periodically review memory, queues, active sessions, receipts, and scheduled jobs, and remove data that should not persist. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ThinkOffApp/ide-agent-kit) <br>
- [Project Homepage](https://github.com/ThinkOffApp/ide-agent-kit) <br>
- [npm Package](https://www.npmjs.com/package/ide-agent-kit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe local files, command allowlists, webhook settings, credentials, queues, receipts, memory, and scheduled jobs.] <br>

## Skill Version(s): <br>
0.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
