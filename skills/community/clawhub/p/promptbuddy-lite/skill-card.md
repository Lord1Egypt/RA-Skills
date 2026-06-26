## Description: <br>
Promptbuddy Lite is a zero-dependency Shell skill that rewrites user prompts into a four-layer HMAW-style structure for role, task, format, and constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steventsang18](https://clawhub.ai/user/steventsang18) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to pre-process broad chat requests into structured prompts before sending them to an assistant. It is suited to lightweight prompt optimization workflows on Linux or macOS where a local Shell implementation is preferred. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The preprocessing wrapper can automatically rewrite broad chat input before it reaches the assistant. <br>
Mitigation: Review the generated structured prompt before relying on it, and disable or bypass preprocessing for prompts where exact wording must be preserved. <br>
Risk: The installer writes commands under /usr/local/bin and requires sudo. <br>
Mitigation: Inspect the installer before execution and install only in environments where system-wide command placement is acceptable. <br>
Risk: The feedback path can invoke an undeclared promptbuddy-optimizer helper when present. <br>
Mitigation: Enable feedback collection only after reviewing the helper skill and confirming its local data handling. <br>


## Reference(s): <br>
- [Promptbuddy Lite on ClawHub](https://clawhub.ai/steventsang18/promptbuddy-lite) <br>
- [HMAW: Hierarchical Multi-Agent Workflows for Zero-Shot Prompt Optimization](https://arxiv.org/abs/2405.20252) <br>
- [The Prompt Report](https://arxiv.org/abs/2406.06608) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the core command and Markdown-like structured prompt text from the preprocessing wrapper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Shell execution; may store prompt-optimization metadata for feedback without preserving the original user input.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
