## Description: <br>
Manage multiple git repositories with a daemon model for periodic add, commit, pull, and push workflows on macOS launchd or Linux systemd. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samwei12](https://clawhub.ai/user/samwei12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure, run, and troubleshoot automated git syncing for multiple repositories, including repository registration and service lifecycle management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The daemon can persistently add, commit, pull, and push registered repositories, which can publish unintended unignored files or incorrect changes. <br>
Mitigation: Run a one-time sync first, register only intended repositories, review ignore rules and pending changes, and add repositories gradually. <br>
Risk: Linux service installation can create a persistent systemd unit and may run with elevated privileges if installed as root. <br>
Mitigation: Prefer a least-privileged user service, avoid running the daemon as root unless explicitly intended, and review any service unit name override before installation. <br>
Risk: Automated sync depends on non-interactive git and SSH credentials for the service identity. <br>
Mitigation: Use the same service user that owns the repositories and credentials, verify git user configuration, and preconfigure trusted SSH host keys before enabling daemon mode. <br>


## Reference(s): <br>
- [Git Sync Daemon Skill Page](https://clawhub.ai/samwei12/git-sync-daemon) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Control CLI Script](artifact/scripts/git_sync_ctl.sh) <br>
- [Daemon Script](artifact/scripts/git_sync_daemon.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference bundled shell scripts, repository list entries, daemon runtime paths, and launchd or systemd service configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
