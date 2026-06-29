## Description: <br>
Guides agents to write concise, structured memory handoff notes when a session discovers durable knowledge such as architecture decisions, root causes, setup gotchas, workflow changes, security findings, reusable patterns, or explicit handoff requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to preserve durable session knowledge as reviewable markdown handoff notes for a memory owner, teammate, or future session. It is useful when findings should be routed into a long-term memory system without editing canonical memory files directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated handoff notes may persist sensitive context in the repository. <br>
Mitigation: Review handoffs before sharing them or ingesting them into a long-term memory system, especially after sessions involving sensitive context. <br>
Risk: Low-value or unverifiable handoffs can pollute durable memory. <br>
Mitigation: Keep handoffs specific and verifiable, include exact paths or commands where relevant, and use the skill's verification guidance before routing the note. <br>


## Reference(s): <br>
- [brigade](https://github.com/escoffier-labs/brigade) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, files, shell commands, guidance] <br>
**Output Format:** [Markdown handoff note with structured sections and optional shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Handoff notes are expected to be specific, verifiable, and under 400 words.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
