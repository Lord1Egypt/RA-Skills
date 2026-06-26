## Description: <br>
Checks and updates OpenClaw skills installed from GitHub with retained git metadata, including branch-based and tag-based skill directories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viccwang](https://clawhub.ai/user/viccwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw workspace maintainers use this skill to inspect local skills installed via GitHub git clone, identify whether they are behind their remote source, and update them when the repository state is safe. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify local git-cloned skill directories by fetching from remotes, fast-forwarding branches, or checking out newer tags. <br>
Mitigation: Run the check command before updating, confirm the target path and git remote, review upstream changes when possible, and keep a rollback path for important workflows. <br>
Risk: Updating a repository in a dirty, ahead, diverged, detached, or unsupported state can confuse or overwrite local work if forced outside the skill's normal safeguards. <br>
Mitigation: Respect the reported stop statuses and resolve local changes, divergent history, or unsupported install methods before attempting an update. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/viccwang/github-skill-updater) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, json, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports update status values such as up-to-date, update-available, dirty, ahead, diverged, and unsupported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
