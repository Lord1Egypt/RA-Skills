## Description: <br>
Context Compressor compresses the current conversation history into a shorter continuation prompt while preserving system instructions and recent messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[relunctance](https://clawhub.ai/user/relunctance) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to reduce long active conversations into compact continuation prompts when context approaches capacity. It is intended for current-session compression rather than cross-session memory management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation-derived content may be retained locally in memory/today.md. <br>
Mitigation: Use dry-run first, avoid sensitive conversations unless local retention is acceptable, and remove retained history when it is no longer needed. <br>
Risk: The installer changes ~/.bashrc and creates a ~/bin symlink to a command target that is not present in the reviewed package. <br>
Mitigation: Inspect or skip the installer, and create any command link manually only after verifying the target script exists. <br>
Risk: Aggressive compression can drop or summarize older details that may still matter. <br>
Mitigation: Review the compressed output before replacing the working context, and use lighter compression or a larger keep-recent setting for high-stakes work. <br>


## Reference(s): <br>
- [Compression Logic](references/compression-logic.md) <br>
- [Auto-Trigger](references/auto-trigger.md) <br>
- [Structured Output](references/structured-output.md) <br>
- [CLI Reference](references/cli.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and structured JSON examples; compressed conversations are represented as text prompts or JSON objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports light, normal, heavy, and emergency compression levels, dry-run preview, recent-message retention settings, token estimates, and optional compression history written to memory/today.md.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
