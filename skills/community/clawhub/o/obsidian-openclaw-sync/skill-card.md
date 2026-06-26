## Description: <br>
Sync Obsidian OpenClaw config across multiple iCloud devices. Manages symlinks for seamless multi-device sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boyd4y](https://clawhub.ai/user/boyd4y) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users on macOS use this skill to inspect iCloud-hosted Obsidian vaults and link OpenClaw configuration, media, projects, team files, skills, and workspaces into a local OpenClaw setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running setup with --overwrite can replace a local openclaw.json with a symlink to the iCloud version. <br>
Mitigation: Run status first, verify the selected vault and paths, and back up any local openclaw.json before using --overwrite. <br>
Risk: Running setup with --no-confirm skips the confirmation prompt before creating symlinks. <br>
Mitigation: Avoid --no-confirm until the vault index and planned symlink targets have been reviewed. <br>


## Reference(s): <br>
- [OpenClaw Vault Structure Reference](references/vault-structure.md) <br>
- [Sync Helper Script](scripts/sync_helper.py) <br>
- [ClawHub Skill Page](https://clawhub.ai/boyd4y/obsidian-openclaw-sync) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text with status listings, prompts, and symlink setup or removal actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS-only; requires Python and an iCloud Obsidian vault path.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
