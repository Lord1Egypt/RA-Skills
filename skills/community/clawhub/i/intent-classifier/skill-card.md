## Description: <br>
意图分类器实时分析用户输入，识别代码、知识、任务、闲聊等意图并建议对应的处理流程或技能路由。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to classify user requests and select an appropriate downstream skill or workflow for code work, knowledge questions, task execution, or chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Intent classifications or routing recommendations may be inaccurate or over-eager. <br>
Mitigation: Treat classifications as suggestions and require explicit confirmation before any routed downstream skill runs commands, edits or deletes files, searches private memory, or performs multi-step automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/intent-classifier) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/534422530) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown intent classification with confidence, trigger features, routing recommendation, and alternatives] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Classification is advisory and should be confirmed before downstream skills perform file, command, memory, or multi-step automation actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
