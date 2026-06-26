## Description: <br>
人物关系与平台昵称管理器。当需要给某人发消息、但不知道对方在某平台的昵称时触发。自动查询记忆，如果没有记录则询问用户并记忆。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calvin-dean](https://clawhub.ai/user/calvin-dean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to resolve a person's platform-specific nickname before sending a message. If no record exists, the agent asks the user for identifying details and platform handles, then stores the profile for future lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an assistant to save persistent personal contact profiles with more data than needed. <br>
Mitigation: Ask for clear user intent, store only the minimum platform handle needed, avoid unnecessary legal names, gender, or relationship notes, and confirm the resolved recipient before sending messages. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Markdown instructions and natural-language responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce contact lookup guidance, clarification questions, and memory entries for later use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
