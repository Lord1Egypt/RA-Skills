## Description: <br>
按需记忆检索。当用户询问历史相关问题时，自动搜索 memory 和 QMD 获取相关信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aeoleader](https://clawhub.ai/user/aeoleader) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People using an OpenClaw agent use this skill to retrieve prior QMD and memory entries when they ask history-related questions, then receive organized results without loading memory into every conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad history-related prompts may surface prior local memory or QMD history that contains sensitive information. <br>
Mitigation: Review stored memory sources before use, avoid storing secrets in memory, and ask the agent to confirm before searching when tighter control is needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with summarized search results and inline shell commands when retrieval is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search is triggered only for history-related prompts and may use QMD search first with memory-file search as a fallback.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
