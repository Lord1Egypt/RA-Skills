## Description: <br>
Adds freshness warnings to OpenClaw memory search results and guides agents to verify older memory entries before relying on them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicshliu](https://clawhub.ai/user/nicshliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add memory freshness checks and verification guidance to agent workflows. It helps agents treat older memory entries cautiously and confirm file, function, or configuration references before acting on them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may rely on outdated memory content or verify memory claims against local files referenced by those memories. <br>
Mitigation: Review the proposed system prompt before adding it to OpenClaw configuration, and keep verification focused on intended project files before using memory-derived claims. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nicshliu/openclaw-memory-freshness) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with configuration snippets and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no external services or credentials are required by the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
