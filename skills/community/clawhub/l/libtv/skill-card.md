## Description: <br>
将《寻秦记》小说文本转换为 web-toon 风格漫画页面，并返回每页 PNG 路径和文字说明。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[treelounge](https://clawhub.ai/user/treelounge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents can use this skill to turn a UTF-8 story or chapter text file into a small set of comic-style PNG pages with accompanying text descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on pinned Python packages, including libtv, that execute locally when installed. <br>
Mitigation: Install and run it in an isolated environment where those dependencies are trusted. <br>
Risk: Generated files are written to a caller-provided output directory. <br>
Mitigation: Choose an output directory that does not contain important files and review generated paths before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/treelounge/libtv) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration] <br>
**Output Format:** [JSON result containing generated PNG image paths and text descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a UTF-8 story file and uses panel count, font, and output directory parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
