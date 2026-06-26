## Description: <br>
每周一键更新PPT讲师备注，从教案中提取讲师活动，自动写入对应PPT幻灯片备注。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuxixixi](https://clawhub.ai/user/wuxixixi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators or course-maintenance agents use this skill to update PowerPoint speaker notes by extracting instructor-activity content from matching Word lesson plans in local course folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process local course folders and create updated PowerPoint copies in those folders. <br>
Mitigation: Review the target course directory and planned input and output files before execution. <br>
Risk: The artifact may automatically install python-pptx if it is missing. <br>
Mitigation: Preinstall python-pptx from a trusted package source before running the skill. <br>
Risk: Weekly automation could run against an unintended directory if configured incorrectly. <br>
Mitigation: Enable scheduling only after confirming the target directory and expected file naming pattern. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuxixixi/ppt-lecture-notes) <br>
- [Publisher profile](https://clawhub.ai/user/wuxixixi) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples; runtime output is updated .pptx files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates updated PowerPoint copies next to the original files and preserves existing notes unless forced.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
