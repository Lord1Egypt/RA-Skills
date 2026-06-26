## Description: <br>
Item Management records, organizes, searches, reports on, exports, backs up, and restores personal item inventory data through natural-language commands and a local CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmmg55](https://clawhub.ai/user/gmmg55) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and assistants use this skill to maintain a local personal inventory, including item details, costs, locations, expiry and warranty dates, history, backups, restores, exports, and printable reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores item names, prices, locations, notes, and dates in a local database and plain JSON backups. <br>
Mitigation: Treat the database, exports, reports, and backups as private files; store them only in trusted local or cloud locations. <br>
Risk: Backup restore can replace or merge inventory data. <br>
Mitigation: Create a fresh trusted backup before restore operations and verify the selected backup file before using full restore. <br>
Risk: The info command can reveal personal filesystem paths. <br>
Mitigation: Avoid sharing terminal output from storage-info commands when it includes private user paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gmmg55/item-management) <br>
- [Publisher profile](https://clawhub.ai/user/gmmg55) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Chinese Markdown and CLI output, with optional CSV, JSON, and HTML export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local SQLite data and can create plain JSON backups, restore files, and printable HTML reports.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
