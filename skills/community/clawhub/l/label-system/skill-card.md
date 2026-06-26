## Description: <br>
构建领域业务标签体系，按业务阶段与场景对拆分知识问答进行分类、打标，并指出知识拆分问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dluolan](https://clawhub.ai/user/dluolan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge-base operators, and domain analysts use this skill to build business label systems from user-provided Excel knowledge exports, apply labels to split question-answer records, and flag split-knowledge quality issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided Excel files may contain sensitive business or personal information. <br>
Mitigation: Review the Excel files before use and remove fields that are not needed for building and applying labels. <br>
Risk: Generated labels or split-knowledge corrections may be inaccurate if domain context is incomplete. <br>
Mitigation: Confirm the domain name, core business areas, and any existing label system before applying labels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dluolan/label-system) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown label-system documentation and Excel tagging results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May add a business-label column to the user's source Excel file and include split-knowledge review notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
