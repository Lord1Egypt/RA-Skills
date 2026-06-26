## Description: <br>
OPC Journal is a CLI-style skill for One Person Company growth journaling, local entry storage, search, export, milestone candidate detection, task tracking, and raw signal extraction for caller-led analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coidea](https://clawhub.ai/user/coidea) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to maintain a local OPC growth journal, record and search entries, export journal data, track simple tasks, and provide structured journal context for an agent to interpret. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private journal contents can be exported to arbitrary local paths. <br>
Mitigation: Review export paths before execution, prefer the default local customer directory, and avoid sensitive or shared filenames. <br>
Risk: Analysis and insight commands can return raw journal text to the calling agent. <br>
Mitigation: Use the skill only with agents and users authorized to handle the journal contents. <br>
Risk: Delete and archive clear operations are intentionally destructive when run with --force. <br>
Mitigation: Treat --force as an explicit confirmation step and verify the target customer ID and entry ID before running destructive commands. <br>


## Reference(s): <br>
- [OPC Journal on ClawHub](https://clawhub.ai/coidea/opc-journal) <br>
- [coidea publisher profile](https://clawhub.ai/user/coidea) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command results with status, result, and message fields; export commands can write Markdown or JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primarily local filesystem output under the OpenClaw customer directory, with caller-selected export paths supported.] <br>

## Skill Version(s): <br>
2.5.2 (source: server release evidence and SKILL.md body) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
