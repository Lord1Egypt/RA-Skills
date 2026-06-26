## Description: <br>
Parse and generate MLSCP (Micro LLM Swarm Communication Protocol) commands for efficient agent-to-agent communication, compressed command parsing, and token-efficient instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sirkrouph-dev](https://clawhub.ai/user/sirkrouph-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to parse, validate, and generate compact MLSCP commands for agent-to-agent task communication. It is suited to workflows that need concise command notation before commands are expanded and reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compact MLSCP commands from other agents may describe file or variable changes too tersely for safe direct execution. <br>
Mitigation: Expand incoming commands into plain language, review the target and intended action, and approve the change before applying it. <br>
Risk: Referenced scripts or Python packages may have behavior that is not represented in the instruction-only skill artifact. <br>
Mitigation: Inspect and scan any separately obtained scripts or packages before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sirkrouph-dev/mlscp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline command and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces compact protocol commands and explanatory guidance; no runtime execution is performed by the skill itself.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
