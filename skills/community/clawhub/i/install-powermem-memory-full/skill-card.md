## Description: <br>
Guides agents through installing and configuring the PowerMem long-term memory plugin for OpenClaw, including prerequisites, CLI or HTTP setup, auto-capture and auto-recall options, verification, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teingi](https://clawhub.ai/user/teingi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up PowerMem as an OpenClaw long-term memory backend. It helps configure persistent local or HTTP-backed memory, verify installation health, and troubleshoot common setup failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can save conversation details into persistent memory and recall them in later turns. <br>
Mitigation: Review autoCapture and autoRecall settings before enabling the plugin, and avoid storing secrets or regulated data unless approved. <br>
Risk: The setup path may run upstream PowerMem or plugin installation commands. <br>
Mitigation: Verify the upstream PowerMem package and memory-powermem installer before running commands, and install in a controlled Python environment when possible. <br>
Risk: Memory data may be stored in a local SQLite database or exposed through an HTTP PowerMem server. <br>
Mitigation: Confirm the intended storage path or server endpoint, protect any HTTP API key, and restrict access to the memory database or service. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/teingi/install-powermem-memory-full) <br>
- [PowerMem Memory Guide](artifact/SKILL.md) <br>
- [Config & Commands Quick Reference](artifact/config-reference.md) <br>
- [PowerMem Introduction](artifact/powermem-intro.md) <br>
- [PowerMem project](https://github.com/oceanbase/powermem) <br>
- [memory-powermem installation guide](https://github.com/ob-labs/memory-powermem/blob/main/INSTALL.md) <br>
- [PowerMem environment example](https://github.com/oceanbase/powermem/blob/master/.env.example) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend installing PowerMem, changing OpenClaw configuration, and enabling persistent conversation memory.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
