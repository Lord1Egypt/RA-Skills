## Description: <br>
Helps agents install, update, diagnose, configure, fix, and tune local OpenClaw installations, including gateway, channel, model failover, authentication, routing, plugin, and configuration issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rendrag-git](https://clawhub.ai/user/rendrag-git) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and support engineers use this skill to troubleshoot and maintain local OpenClaw installations. It guides read-only diagnosis, safe configuration edits, service verification, docs lookup, plugin repair, and incident recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad local administration of OpenClaw, including diagnostics and proposed service or configuration changes. <br>
Mitigation: Install it only for trusted agents and review confirmations before restarts, deletes, token changes, plugin changes, or docs-cache refreshes. <br>
Risk: OpenClaw environments may contain secrets, OAuth material, private sessions, and agent workspace contents. <br>
Mitigation: Do not allow the skill to read secret files or private session contents unless the scope is explicitly narrowed and approved. <br>
Risk: Incorrect config edits can break gateway startup or channel routing. <br>
Mitigation: Use the skill's backup, narrow-edit, validation, and post-change verification workflow before treating a repair as complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rendrag-git/openclawadmin) <br>
- [OpenClaw documentation](https://docs.openclaw.ai/) <br>
- [OpenClaw docs index](https://docs.openclaw.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local diagnostics, config edits, backups, service checks, plugin repairs, and docs-cache refresh steps for user review.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
