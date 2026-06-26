## Description: <br>
Memory Guardian helps AI agents monitor memory health, detect context growth and stale files, manage session-to-permanent memory promotion, and recover from memory corruption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dodge1218](https://clawhub.ai/user/dodge1218) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep long-running agent memory organized, detect unhealthy memory growth, identify stale or duplicate memory files, and plan safe promotion or recovery work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill text directs agents to preserve credentials or keys in permanent memory. <br>
Mitigation: Do not store raw API keys, passwords, tokens, private keys, or credentials in agent memory; store only non-sensitive references and use a dedicated secret manager. <br>
Risk: The workflow discusses deleting stale session files and restoring memory from git history. <br>
Mitigation: Require explicit user approval plus a backup or diff before deleting session files or restoring memory state. <br>
Risk: The scanner verdict is suspicious because cleanup and rollback guidance lacks sufficient safeguards. <br>
Mitigation: Treat the included script as diagnostic by default and add approval gates before enabling any automated cleanup behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dodge1218/memory-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and plain-text diagnostic reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The diagnostic script reads OpenClaw memory files under OPENCLAW_WORKSPACE or ~/.openclaw/workspace; deletion, cleanup, or restore actions should require explicit approval and a backup or diff.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
