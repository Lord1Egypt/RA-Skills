## Description: <br>
Synchronizes an OpenClaw workspace, including memory, identity, tool configuration, custom skills, and related files, to a GitHub repository for backup, version control, restore, and server migration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davinwang](https://clawhub.ai/user/davinwang) <br>

### License/Terms of Use: <br>
GNU General Public License v3.0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to back up, restore, inspect, and migrate workspace memory and configuration through a GitHub repository. It is intended for users who intentionally want full or memory-only workspace synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload sensitive OpenClaw identity, memory, tool configuration, skills, and related workspace files to GitHub. <br>
Mitigation: Use only a private repository that you own, review the exact files before pushing, and choose memory-only mode when a full workspace backup is not required. <br>
Risk: GitHub tokens may be exposed if they are placed in shell profiles, inline cron entries, logs, or shared configuration. <br>
Mitigation: Use a fine-grained token limited to the target repository, avoid storing the token in shared dotfiles or inline cron commands, and rotate tokens regularly. <br>
Risk: The cron helper includes a default repository value that may not match the user's intended backup destination. <br>
Mitigation: Set GITHUB_REPO explicitly before enabling scheduled backups and confirm the destination repository in logs before relying on automation. <br>
Risk: Restore operations can overwrite local workspace files. <br>
Mitigation: Keep a local backup before pulling or migrating, inspect differences first, and test restore into a temporary workspace when possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/davinwang/github-memory-sync) <br>
- [README.md](README.md) <br>
- [CRON.md](CRON.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run Git operations against the configured repository and may write restored files into the configured workspace.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
