## Description: <br>
Structured learning pipeline with quality-gated promotion. Captures corrections, errors, and patterns; promotes only what proves itself through recurrence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msruruguay](https://clawhub.ai/user/msruruguay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to capture corrections, errors, knowledge gaps, best practices, and recurring patterns, then promote repeated high-value learnings into project memory. It is intended for teams that want structured agent self-improvement with deduplication, scoring, staging, and pruning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to persist learning data and promote rules into future agent instructions without enough user approval controls. <br>
Mitigation: Require manual approval and diff review before any promotion into CLAUDE.md, AGENTS.md, or permanent memory. <br>
Risk: Persisted learning stores may retain sensitive, stale, or low-value information over time. <br>
Mitigation: Add secret redaction and periodically prune the .learnings, .patterns, and .knowledge stores. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/msruruguay/midos-self-improver) <br>
- [MidOS](https://midos.dev) <br>
- [MidOS Developer Access](https://midos.dev/dev) <br>
- [MidOS Pro](https://midos.dev/pro) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, and JSON entry examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project-local learning records and promoted memory instructions when adopted by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.json, changelog, released 2026-03-04) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
