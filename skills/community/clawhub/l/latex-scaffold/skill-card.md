## Description: <br>
Scaffold LaTeX papers into modular structure for organizing .tex files, generating figure code, and table highlighting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[instinct323](https://clawhub.ai/user/instinct323) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and academic authors use this skill to structure LaTeX paper projects, split content into modular source files, generate figure snippets for image assets, and add table highlighting definitions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The asset-generation script writes new .tex files in the selected project's assets directory. <br>
Mitigation: Run the script only against the intended project root and review generated snippets before building or committing them. <br>
Risk: The skill points users to an external IEEE template ZIP when no LaTeX project exists. <br>
Mitigation: Verify the download source and inspect the ZIP contents before using the template. <br>


## Reference(s): <br>
- [LaTeX Scaffold on ClawHub](https://clawhub.ai/instinct323/latex-scaffold) <br>
- [IEEE conference template ZIP](https://ras.papercept.net/conferences/support/files/ieeeconf.zip) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with LaTeX and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create .tex snippets next to image files under a project's assets directory when the bundled script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
