## Description: <br>
Scan, deduplicate, and organize files in a directory by type, generating a dry-run plan before optionally moving files without deleting anything. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to inspect cluttered local folders, find duplicate files, generate organization plans, optionally move files into type-based folders, and produce inventory or before/after reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skip-confirmation execution mode can overwrite existing destination files despite the skill's conservative default posture. <br>
Mitigation: Run a dry run first, inspect destination conflicts, keep backups, and avoid --execute --yes unless overwrites are intentional. <br>
Risk: Generated inventories and reports can expose private local file names, paths, timestamps, and folder structure. <br>
Mitigation: Treat generated JSON and Markdown reports as private and review them before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/newageinvestments25-byte/nai-file-organizer) <br>
- [File category mappings](artifact/references/categories.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON inventories and plans, and Markdown manifest reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run plans are the default; execution requires an explicit flag and generated reports may include local file names and paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
