## Description: <br>
Hui-Yi manages a file-based cold-memory archive under memory/cold/ and supports an optional opt-in local hook for recall-related session signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuetsui](https://clawhub.ai/user/fuetsui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Hui-Yi to create, search, review, resurface, and maintain durable low-frequency memory notes without promoting every historical detail into primary memory. It is suited to explicit requests for historical continuity, cold-memory recall, cooling, rebuild, and repetition-driven reinforcement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a persistent local cold-memory tool that creates or modifies files under memory/cold/ and memory/heartbeat-state.json. <br>
Mitigation: Install and run it only when a persistent local archive is desired, and review changes to cold-memory notes, tags, indexes, and heartbeat state. <br>
Risk: The optional hook can persist recall-related activation metadata from real conversations once installed and enabled. <br>
Mitigation: Review the hook template before running scripts/install_hook.py --enable, keep HUI_YI_HOOK_DEBUG unset except during brief troubleshooting, and disable the hook in openclaw.json when signal updates are not wanted. <br>
Risk: Enabling the hook changes OpenClaw hook configuration. <br>
Mitigation: Use the installer's dry-run and disclosure path first; the installer is expected to refuse creating a missing openclaw.json. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fuetsui/hui-yi) <br>
- [Cold Memory Schema Reference](artifact/references/cold-memory-schema.md) <br>
- [Cold Memory Examples](artifact/references/examples.md) <br>
- [Heartbeat Cooling Playbook](artifact/references/heartbeat-cooling-playbook.md) <br>
- [Trigger Modes + Integration Patterns](artifact/references/integration-patterns.md) <br>
- [Real Session Signals Integration Design](artifact/references/real-session-signals-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local cold-memory files and optional hook configuration when the user runs the provided scripts.] <br>

## Skill Version(s): <br>
1.2.11 (source: server release evidence and artifact manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
