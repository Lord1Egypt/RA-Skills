## Description: <br>
Automated GitHub synchronization for Obsidian vaults with conflict detection and notification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Leo-zzl](https://clawhub.ai/user/Leo-zzl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and Obsidian users use this skill to configure a Git-backed backup and synchronization workflow for an Obsidian vault, including scheduled syncs and conflict checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A misconfigured vault path or GitHub remote could sync the wrong notes or publish private content. <br>
Mitigation: Confirm OBSIDIAN_VAULT_DIR and GITHUB_REMOTE_URL, use a private or intended repository, and test the script manually before scheduling it. <br>
Risk: The sync script stages all vault changes, which can include secrets, cache files, or plugin state if the vault is not filtered. <br>
Mitigation: Review .gitignore exclusions and avoid storing secrets in synced notes before enabling automatic commits. <br>
Risk: Scheduled sync jobs can continue running after the user forgets they were enabled. <br>
Mitigation: Track any cron, OpenClaw, or systemd timer created for the sync workflow and disable it when no longer needed. <br>


## Reference(s): <br>
- [Setup Guide](references/setup-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Leo-zzl/obsidian-github-sync) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps and operational commands for local Git, cron, OpenClaw, or systemd workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
