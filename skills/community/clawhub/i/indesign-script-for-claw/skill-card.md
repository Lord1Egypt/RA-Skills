## Description: <br>
Generates Adobe InDesign automation scripts for general layout and manga typesetting, with Windows and macOS workflows for configuring and running bundled InDesign scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jqk4388](https://clawhub.ai/user/jqk4388) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, manga localization teams, and automation developers use this skill to generate or run Adobe InDesign ExtendScript workflows for batch layout changes, image placement, text import, style application, and manga lettering automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can run local shell, PowerShell, Python helper, and InDesign scripts from configurable or project-adjacent paths. <br>
Mitigation: Review generated scripts, configuration files, adjacent launchers, and segmentation.pythonScriptPath before execution; run only in trusted project folders. <br>
Risk: Manuscript paths, processing details, or text may be written to local temporary files or logs during automation. <br>
Mitigation: Avoid processing sensitive unpublished manuscripts unless local temp-file and log behavior is acceptable, and clear generated logs when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jqk4388/indesign-script-for-claw) <br>
- [Publisher profile](https://clawhub.ai/user/jqk4388) <br>
- [Homepage from release metadata](https://github.com/jqk4388/Mangahanhua-Scripts-for-Indesign/tree/master/Indesign-script-for-claw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSX/JavaScript, shell or PowerShell commands, and JSON configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for Adobe InDesign CC 2023+ workflows and ES3-compatible ExtendScript where applicable.] <br>

## Skill Version(s): <br>
1.1.51 (source: server release metadata; artifact frontmatter reports 1.1.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
