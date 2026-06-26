## Description: <br>
Automatically monitors and optimizes conversation context by summarizing key points, preserving facts, and reducing old context to help prevent prompt size errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blackworm](https://clawhub.ai/user/blackworm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to manage long-running conversations by summarizing important context, writing selected facts to memory, and keeping recent messages available. It also provides commands for manual context optimization and large-task splitting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic memory updates can preserve sensitive or unwanted conversation details. <br>
Mitigation: Review configuration before installing, disable automatic memory updates when not needed, and avoid using the skill on conversations containing secrets or sensitive personal or business data. <br>
Risk: Automatic cleanup can prune conversation context that may still be needed. <br>
Mitigation: Disable scheduled cleanup or automatic purging unless explicitly desired, and review retention settings before running the skill. <br>
Risk: The optimization command may report successful optimization while processing mock messages instead of the real session. <br>
Mitigation: Verify integration with the actual conversation history before relying on command output for operational decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/blackworm/optimize-context) <br>
- [Publisher Profile](https://clawhub.ai/user/blackworm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, command output, JSON configuration, and memory file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create context summary files, update MEMORY.md, and return optimized message sets when integrated with a context monitor.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
