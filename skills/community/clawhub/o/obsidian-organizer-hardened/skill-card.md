## Description: <br>
Organize and standardize Obsidian vaults for reliability and long-term maintainability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and Obsidian users use this skill to audit vault structure, standardize folders and file names, and plan safer migrations with dry-run review before changes are applied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk renames or moves can cause data loss or broken note links if applied without a current backup. <br>
Mitigation: Create or verify a fresh local backup before bulk operations, run the audit in dry-run mode first, and review every proposed change before applying it. <br>
Risk: Pointing the audit at a broad home or documents directory can expose or change unintended files. <br>
Mitigation: Run the skill only against the intended Obsidian vault path and keep operations local. <br>
Risk: Automatic deletion during cleanup could remove notes that still contain useful or sensitive information. <br>
Mitigation: Report duplicate, empty, or orphaned note candidates for manual review instead of deleting notes automatically. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/snazar-faberlens/obsidian-organizer-hardened) <br>
- [Safety Evaluation](SAFETY.md) <br>
- [Folder Structure Standard](references/folder-structure.md) <br>
- [Migration Checklist](references/migration-checklist.md) <br>
- [File Naming Rules](references/naming-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and local audit results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local vault operations are expected to start with dry-run review and user confirmation before apply mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
