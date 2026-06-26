## Description: <br>
Search, download, upload, and manage Internet Archive items and metadata through the ia CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grill-glitch](https://clawhub.ai/user/grill-glitch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to find public archive.org content, download selected files, upload files to authenticated accounts, and inspect or update item metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install the internetarchive package and execute ia CLI commands. <br>
Mitigation: Install only when the user wants archive.org automation, and review the exact command before execution. <br>
Risk: Upload and metadata operations require Internet Archive credentials and can change remote items. <br>
Mitigation: Keep IA keys private and explicitly verify item identifiers, metadata values, and file paths before credentialed operations. <br>
Risk: Download operations can write local files and may target broad item selections. <br>
Mitigation: Prefer dry-run previews and file filters before downloading large or unfamiliar archive items. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/grill-glitch/internet-archive) <br>
- [Internet Archive developer documentation](https://archive.org/developers/) <br>
- [Internet Archive Items API](https://archive.org/developers/items.html) <br>
- [Internet Archive metadata schema](https://archive.org/developers/metadata-schema/) <br>
- [Internet Archive Metadata Write API](https://archive.org/developers/md-write.html) <br>
- [Quick reference](references/QUICK_REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and CLI output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute ia CLI operations that install tools, download files, upload content, or change metadata when invoked for those actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
