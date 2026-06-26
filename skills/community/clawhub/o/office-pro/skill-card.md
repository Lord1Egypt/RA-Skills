## Description: <br>
Enterprise document automation suite for AI Agents that generates Word contracts, Excel reports, and report documents with built-in templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deki18](https://clawhub.ai/user/deki18) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI agent users and developers use Office Pro to create Chinese-language business contracts, spreadsheets, and routine reports from structured inputs without supplying external templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated contracts, reports, and spreadsheets may contain incomplete or inappropriate business or legal content for the user's situation. <br>
Mitigation: Review generated documents before use, especially contracts or records that affect legal, financial, or employment decisions. <br>
Risk: Generated files are written to local output paths and may overwrite or expose sensitive business data if paths are chosen carelessly. <br>
Mitigation: Run the skill in a controlled workspace and provide explicit safe output filenames and directories. <br>
Risk: The skill depends on Python document-generation libraries that must be installed in the agent environment. <br>
Mitigation: Install python-docx and openpyxl in a virtual environment before use. <br>


## Reference(s): <br>
- [ClawHub Office Pro release](https://clawhub.ai/deki18/office-pro) <br>
- [ClawHub publisher profile: deki18](https://clawhub.ai/user/deki18) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python API examples and generated Word or Excel files when executed by an agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files are written locally; callers can provide output filenames and directories.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata; artifact frontmatter reports 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
