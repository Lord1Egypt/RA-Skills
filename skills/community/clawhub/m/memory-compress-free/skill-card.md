## Description: <br>
日志压缩器免费版 helps agents compress a single Markdown log file into a structured summary for memory maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to summarize daily Markdown logs, extract key events and todos, and decide whether to append the reviewed summary to persistent memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review notes inconsistent documentation about whether logs stay local. <br>
Mitigation: Use the skill only on logs that are acceptable for the agent runtime or model provider to process. <br>
Risk: The artifact directs persistent MEMORY.md updates after compression. <br>
Mitigation: Manually inspect the generated summary before appending it to persistent memory. <br>
Risk: The artifact references a compression script path, but the provided artifact contains only SKILL.md. <br>
Mitigation: Verify that the actual compression script exists and matches the intended command before running any shell command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/memory-compress-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured summaries from one input log file; manual review is expected before updating persistent memory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
