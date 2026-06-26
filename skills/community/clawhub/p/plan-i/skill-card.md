## Description: <br>
启动一个新的规划流程，创建新的规划文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[9talk](https://clawhub.ai/user/9talk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to start a new planning workflow, create a dated local planning Markdown file, and record an initial structured planning draft before handing off to the next planning step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes an initial planning draft to a local Markdown file immediately. <br>
Mitigation: Review the generated planning file before using it in follow-on planning steps. <br>
Risk: Planning requests may contain sensitive project details that would be persisted in the generated file. <br>
Mitigation: Avoid including secrets or unnecessary sensitive information in the planning request. <br>
Risk: The plan name is used in the generated file path. <br>
Mitigation: Use a simple, descriptive plan name without sensitive content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/9talk/plan-i) <br>
- [Publisher profile](https://clawhub.ai/user/9talk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown planning file plus a concise handoff message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a dated file under plans/ and writes the initial planning draft before returning guidance.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
