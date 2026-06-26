## Description: <br>
Insert mind maps and architecture diagrams into Markdown documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drunkpig](https://clawhub.ai/user/drunkpig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to add mind maps and architecture diagrams to Markdown documents while keeping diagram source files and generated PNGs in a local `.mddoc/` directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose installing or running local tools such as mddoc, d2, npm, brew, or winget. <br>
Mitigation: Review proposed install and build commands before approval, and install dependencies from trusted package sources. <br>
Risk: Broad diagram trigger phrases may activate the skill during casual diagram-related requests. <br>
Mitigation: Confirm the user intends to modify Markdown and create `.mddoc/` files before proceeding. <br>


## Reference(s): <br>
- [D2 installation guide](https://d2lang.com/tour/install) <br>
- [Skill feedback and issues](https://github.com/drunkpig/md-of-programer/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and diagram source snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates `.mddoc/` diagram source files and generated PNG assets alongside the target Markdown file.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
