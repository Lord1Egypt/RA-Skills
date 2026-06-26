## Description: <br>
Adds mind maps or architecture diagrams to Markdown documents when users ask for a mind map, architecture diagram, chart, mind map, or diagram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drunkpig](https://clawhub.ai/user/drunkpig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to create Markdown-adjacent mind map or architecture diagram source files, render PNG diagrams, and insert the resulting image links back into Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask the agent to run global dependency installation commands when mddoc or d2 are missing. <br>
Mitigation: Review dependency installation commands first, or install mddoc and d2 through an approved local process before using the skill. <br>
Risk: The skill creates or modifies Markdown-adjacent diagram files under .mddoc and inserts generated PNG links into Markdown. <br>
Mitigation: Review generated source files, PNG outputs, and inserted Markdown links before committing or publishing the document. <br>


## Reference(s): <br>
- [D2 installation guide](https://d2lang.com/tour/install) <br>
- [ClawHub skill page](https://clawhub.ai/drunkpig/mddoc-design) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, D2 or markmap source files, generated PNG files, and Markdown image links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Diagram source files and generated PNG files are kept under a .mddoc directory next to the Markdown document.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
