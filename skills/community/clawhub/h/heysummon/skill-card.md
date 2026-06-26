## Description: <br>
Request expert help by submitting queries to the HeySummon platform, which routes them to registered human providers for assistance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomasansems](https://clawhub.ai/user/thomasansems) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and their operators use this skill when an automated workflow is stuck and needs help from a named or matching human expert through the HeySummon platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles API keys, local key material, request records, and event logs. <br>
Mitigation: Keep .env, providers.json, .keys, .requests, and logs out of version control, restrict local file permissions, and avoid sending secrets in submitted prompts or context. <br>
Risk: The watcher runs persistently and uses the local OpenClaw gateway token while active. <br>
Mitigation: Review the watcher script before starting it, run it only in trusted workspaces, and stop it when the skill is not in use. <br>
Risk: The optional auto-sync script can commit and push local changes to a git remote. <br>
Mitigation: Disable, remove, or rewrite auto-sync unless the repository hygiene and destination remote have been reviewed. <br>
Risk: Submitted prompts and context are shared with the HeySummon platform and human providers. <br>
Mitigation: Treat requests as external disclosures and redact credentials, private data, and sensitive business context before submission. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/thomasansems/heysummon) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local status text and script-driven configuration or state files when the user runs the provided commands.] <br>

## Skill Version(s): <br>
0.1.0-beta (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
