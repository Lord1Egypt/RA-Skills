## Description: <br>
Layered Memory Manager helps OpenClaw agents maintain a two-tier persistent memory system with search, promotion, demotion, archiving, restoration, and memory health workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chyern](https://clawhub.ai/user/chyern) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep persistent OpenClaw memory accurate, searchable, and size-controlled across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist, reorganize, archive, and sometimes delete memory state through broad natural-language and inline tag triggers. <br>
Mitigation: Review the memory folder before use, avoid storing sensitive personal or credential-like information, and require explicit confirmation for pin, promote, forget, archive, restore, and permanent deletion actions. <br>
Risk: Memory operations can alter what future agent sessions recall or prioritize. <br>
Mitigation: Keep L2 files as the source of truth, review `hygiene.json` logs, and verify L1/L2 sync after memory updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chyern/layered-memory-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with memory file updates and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update MEMORY.md, memory/*.md, memory/archive/, and memory/hygiene.json when the agent applies the workflow.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
