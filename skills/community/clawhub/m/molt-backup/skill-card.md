## Description: <br>
Molt snapshots OpenClaw brain files, memory, cron metadata, and redacted configuration to an offsite git repository controlled by the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robin-marv](https://clawhub.ai/user/robin-marv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Molt to create manual or scheduled backups of OpenClaw brain files, memory directories, cron job exports, and redacted configuration snapshots in a private git repository they control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups can include sensitive OpenClaw brain files, memory, cron metadata, and redacted configuration snapshots. <br>
Mitigation: Use only a private repository you control, inspect generated backup contents before the first push, and avoid broad extra directories unless each path has been reviewed. <br>
Risk: Git credentials or repository URLs may expose access if tokens are embedded directly in command lines or configuration. <br>
Mitigation: Prefer SSH keys or a credential helper instead of tokens in URLs. <br>
Risk: Scheduled backups can continue sending new data after the user no longer needs them. <br>
Mitigation: Remove the cron job when automatic backups are no longer wanted. <br>
Risk: A misconfigured run can push unexpected files or destinations. <br>
Mitigation: Run with --dry-run first and confirm MOLT_REPO_URL, MOLT_DIR, MOLT_WORKSPACE, and MOLT_EXTRA_DIRS before enabling regular pushes. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/robin-marv/molt-backup) <br>
- [Publisher profile](https://clawhub.ai/user/robin-marv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces backup guidance and invokes scripts that create git commits containing selected OpenClaw files, cron exports, and redacted configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
