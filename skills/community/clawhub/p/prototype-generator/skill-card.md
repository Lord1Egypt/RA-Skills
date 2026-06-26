## Description: <br>
Automatically generates backend admin/list prototypes from natural-language requirements, with support for mountListPage-style frameworks, standalone HTML, and project-specific setups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[limingfa](https://clawhub.ai/user/limingfa) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and product engineers use this skill to turn admin or list-page requirements into runnable prototype pages, either integrated with an existing mock UI framework or emitted as standalone HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may scan and edit project files while generating prototypes. <br>
Mitigation: Use it in a version-controlled workspace and review the resulting diff before keeping changes. <br>
Risk: Generated prototype files may not match the intended project structure or framework mode. <br>
Mitigation: Tell the agent whether to create standalone HTML or integrate with an existing mock UI framework, and specify the target directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/limingfa/prototype-generator) <br>
- [Project homepage](https://github.com/limingfa/prototype-skills) <br>
- [Support issues](https://github.com/limingfa/prototype-skills/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Configuration, Guidance] <br>
**Output Format:** [HTML, JavaScript, optional SQL, and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May add or edit prototype files such as menu.js, view_*.html, mock-ui.js, standalone HTML, or optional SQL files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
