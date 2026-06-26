## Description: <br>
Converts Yuque .lakebook exports into organized Markdown and Excel output folders, including rich text, database tables, sheets, attachments, encrypted-content placeholders, and a conversion report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luhuiwang](https://clawhub.ai/user/luhuiwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-management users can use this skill to convert Yuque lakebook exports into portable Markdown, Excel, downloaded asset folders, and a conversion report for review or migration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted .lakebook input can cause unsafe file writes. <br>
Mitigation: Use only trusted .lakebook files and run conversion in a disposable working directory or sandbox. <br>
Risk: The converter can make outbound requests to embedded image and attachment URLs. <br>
Mitigation: Review the source export before conversion and disable or restrict downloads when network access is not expected. <br>
Risk: The startup script can install Python dependencies automatically. <br>
Mitigation: Install and review dependencies explicitly before running the skill instead of relying on automatic installation. <br>
Risk: The converter uses a local ./temp directory during processing. <br>
Mitigation: Run it in a clean directory where an existing ./temp path does not contain data that must be preserved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/luhuiwang/lakebook-to-md) <br>
- [Original YuqueExportToMarkdown project named by the skill docs](https://github.com/PZh101/YuqueExportToMarkdown) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown files, Excel workbooks, downloaded asset folders, and a Markdown conversion report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform outbound downloads for embedded images and attachments when resource downloading is enabled.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, SKILL.md frontmatter, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
