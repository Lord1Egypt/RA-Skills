## Description: <br>
Use this skill for Crowdin requests that read, create, or update project data through the OOMOL Crowdin connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, localization managers, and agent users use this skill to inspect Crowdin projects and perform controlled project updates such as creating branches, creating directories, and uploading source files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crowdin project changes can be made by write actions such as creating branches, creating directories, and uploading source files. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>
Risk: The setup flow can install the OOMOL CLI from a remote installer. <br>
Mitigation: Review the OOMOL CLI installer or use manually verified installation steps before setup. <br>
Risk: Crowdin operations are mediated through OOMOL-connected credentials. <br>
Mitigation: Install only when using OOMOL as an intermediary is acceptable for the workspace and project. <br>


## Reference(s): <br>
- [Crowdin homepage](https://crowdin.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub Crowdin skill page](https://clawhub.ai/oomol/oo-crowdin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Crowdin connector JSON responses when actions are run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
