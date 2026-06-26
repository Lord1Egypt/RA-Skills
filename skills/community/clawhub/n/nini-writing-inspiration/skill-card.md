## Description: <br>
Use when user needs help starting or continuing writing (not diary). Triggers include「不知道写什么」「帮我构思」「写游记」「记录 TIL」「写点什么」. For diary writing, use diary-assistant instead. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niracler](https://clawhub.ai/user/niracler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill when they want help starting or continuing travel writing, TIL notes, or general articles. The agent guides the user through one question at a time, confirms each answer, and organizes the material into prose without taking over the topic direction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate for broad writing-help prompts, including prompts that could be better handled by a diary or journaling skill. <br>
Mitigation: Use a more specific diary or journaling skill when the user intent is personal diary writing. <br>
Risk: Writing prompts can include private personal details if the user chooses to share them. <br>
Mitigation: Avoid sharing private personal details unless they are intended to be part of the conversation. <br>


## Reference(s): <br>
- [Writing framework reference](references/frameworks.md) <br>
- [ClawHub skill page](https://clawhub.ai/niracler/nini-writing-inspiration) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Code, Configuration] <br>
**Output Format:** [Conversational text or Markdown with questions, outlines, draft prose, and TIL snippets when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive sequential question flow; excludes diary writing and redirects diary use to diary-assistant.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
