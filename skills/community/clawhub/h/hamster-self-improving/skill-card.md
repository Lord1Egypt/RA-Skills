## Description: <br>
Self-reflection + Self-criticism + Self-learning + Self-organizing memory. Agent evaluates its own work, catches mistakes, and improves permanently. Use before starting work and after responding to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Theo-jobs](https://clawhub.ai/user/Theo-jobs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture explicit corrections, self-reflections, preferences, and reusable work patterns in a local tiered memory system so future agent sessions can improve with visible, auditable state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory and steering can influence future agent sessions beyond the immediate task. <br>
Mitigation: Use Passive or Strict mode, keep learned rules visible, review memory entries regularly, and remove entries that should no longer affect behavior. <br>
Risk: Sensitive personal, work, credential, financial, medical, third-party, or access-context data could be stored in memory. <br>
Mitigation: Follow the skill's boundaries: do not store those categories, inspect ~/self-improving/ regularly, and use the forget or wipe flows when needed. <br>
Risk: Suggested edits to AGENTS.md, SOUL.md, or HEARTBEAT.md can change agent behavior across sessions. <br>
Mitigation: Review those edits before applying them and keep any inferred rules tentative until the user validates them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Theo-jobs/hamster-self-improving) <br>
- [Skill Homepage](https://clawic.com/skills/self-improving) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Security Boundaries](artifact/boundaries.md) <br>
- [Setup Guide](artifact/setup.md) <br>
- [Memory Operations](artifact/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and maintains local files under ~/self-improving/; no required external binaries are declared.] <br>

## Skill Version(s): <br>
1.2.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
