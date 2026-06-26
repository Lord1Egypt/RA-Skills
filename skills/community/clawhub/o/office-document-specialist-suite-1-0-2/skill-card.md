## Description: <br>
Creates Word report templates and applies professional layout and styling to existing .docx files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lbtylb](https://clawhub.ai/user/lbtylb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and document automation users use this skill to generate a styled Word report template or apply consistent layout, headers, footers, and typography to existing .docx files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release description claims Excel and PowerPoint support, but the security summary identifies the artifact as a Word document helper. <br>
Mitigation: Treat the skill as a Word .docx helper unless future release evidence confirms spreadsheet or slide support. <br>
Risk: Setup installs Python dependencies, and document operations can modify local files. <br>
Mitigation: Run setup in an isolated environment, consider pinning dependency versions, and test on copies of important documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lbtylb/office-document-specialist-suite-1-0-2) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [DOCX files and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or rewrites local .docx files at paths selected by the agent; requires Python 3, python-docx, and lxml.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
