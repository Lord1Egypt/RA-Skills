## Description: <br>
nix-memory helps OpenClaw agents maintain identity and memory continuity by hashing key workspace files, detecting drift, and reporting continuity status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cassh100k](https://clawhub.ai/user/cassh100k) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to baseline agent identity files, monitor workspace memory files, detect drift across sessions, and surface continuity alerts for OpenClaw workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace identity and memory files may contain secrets that are copied, hashed, diffed, or summarized into local .nix-memory state. <br>
Mitigation: Remove secrets from SOUL.md, IDENTITY.md, USER.md, AGENTS.md, MEMORY.md, HEARTBEAT.md, and workspace Markdown files before running setup or quickstart. <br>
Risk: Quickstart can add local helper files and checks, including agent.json, memory scripts, HEARTBEAT.md entries, and session state templates. <br>
Mitigation: Review quickstart before running it and set NIX_MEMORY_WORKSPACE to the intended workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cassh100k/nix-memory) <br>
- [nix-memory docs](https://nixus.pro/memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON reports] <br>
**Output Format:** [Plain text statuses, Markdown guidance, shell command examples, JSON reports, and local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local state under .nix-memory/ and may create helper files such as agent.json, HEARTBEAT.md entries, and memory logs when quickstart is used.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
