## Description: <br>
Renders Mermaid diagrams as terminal ASCII text by default, or exports supported diagrams as PNG images when the user requests image output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallnest](https://clawhub.ai/user/smallnest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and external users can use this skill to turn Mermaid flowcharts, sequence diagrams, class diagrams, pie charts, Git graphs, state diagrams, and ER diagrams into readable terminal output or PNG files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PNG export can create a local image and may use the documented BOS upload behavior, which is privacy-relevant for sensitive diagrams. <br>
Mitigation: Use terminal ASCII mode for sensitive diagrams, and request PNG export only when local file creation and the documented upload behavior are acceptable. <br>


## Reference(s): <br>
- [Mermaid chart types reference](references/chart-types.md) <br>
- [ClawHub release page](https://clawhub.ai/smallnest/mermaid-renderer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Guidance] <br>
**Output Format:** [Terminal ASCII text or PNG image file, typically accompanied by concise Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [PNG export writes a local image file and may use the documented BOS upload behavior when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
