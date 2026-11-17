## Description:

Jarvis Core Main configures an agent as a proactive companion-style assistant with persistent memory, emotional-state modeling, confidence calibration, relationship analysis, and safety boundary routines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angelofalhashmi](https://clawhub.ai/user/angelofalhashmi)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to configure an agent for persistent personal assistance, proactive follow-up, confidence-aware advice, memory recall, and relationship or emotional-context analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad persistent memory, profiling, and proactive behavior may retain sensitive personal context.

Mitigation: Before use, decide which memory files the agent may read or write, keep sensitive memory files out of synced or shared folders, and review stored notes regularly.

Risk: Emotional and relationship logging may create inaccurate or sensitive inferences.

Mitigation: Disable or manually review emotional and relationship logs, and treat stored inferences as editable notes rather than facts.

Risk: Proactive suggestions can be based on stale context or incorrect confidence estimates.

Mitigation: Require confirmation for external or irreversible actions and review high-impact recommendations before acting on them.

## Reference(s):

- [Jarvis Core Main on ClawHub](https://clawhub.ai/angelofalhashmi/skills/jarvis-core-angelofalhashmi)
- [Jarvis Core GitHub repository](https://github.com/davidme6/jarvis-core)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Natural-language and Markdown responses with optional code blocks, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local memory files and logs when the host agent grants file access.]

## Skill Version(s):

3.1.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
