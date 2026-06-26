## Description: <br>
Lobster Autodream helps an agent periodically consolidate conversation history into concise long-term memory notes using time, volume, and quality gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to organize new conversation history, extract durable preferences or decisions, and keep local long-term memory files concise and current. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may change local long-term memory automatically. <br>
Mitigation: Require a visible diff or confirmation before accepting changes to MEMORY.md. <br>
Risk: Conversation history may contain secrets, sensitive personal data, or speculative inferences that should not become durable memory. <br>
Mitigation: Review extracted memories and exclude secrets, sensitive personal data, and unsupported inferences before writing them. <br>
Risk: Memory cleanup could remove or overwrite useful context if the agent misjudges what is outdated. <br>
Mitigation: Review cleanup proposals before deletion and keep memory updates concise, sourced, and easy to revert. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with memory-update recommendations and optional configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose updates to local MEMORY.md and memory/*.md files; review file changes before relying on them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
