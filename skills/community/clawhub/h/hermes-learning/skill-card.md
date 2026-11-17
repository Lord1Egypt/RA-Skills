## Description:

Hermes learning-material synchronization skill that imports self-updated learning materials from Hermes Agent to help WorkBuddy Agent optimize itself, with evolution.db persistence, concept links, and a bidirectional feedback loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuboacean](https://clawhub.ai/user/liuboacean)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to synchronize Hermes Agent learning summaries, strategy data, and feedback reports into WorkBuddy Agent's persistent learning stores. It supports reviewing status, applying learning materials, listing strategies, checking content against avoid patterns, and inspecting feedback analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can import Hermes learning text into WorkBuddy's persistent global memory without enough review, validation, or containment.

Mitigation: Install only when that memory sharing is intended, review ~/.hermes/shared/memory_summary.json before applying learning materials, and avoid unattended daily imports.

Risk: Incorrect or low-quality imported guidance may persist in ~/.workbuddy/memory/evolution.db.

Mitigation: Inspect or delete affected entries from ~/.workbuddy/memory/evolution.db if bad guidance is imported.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/liuboacean/skills/hermes-learning)
- [Publisher profile](https://clawhub.ai/user/liuboacean)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local JSON or SQLite side effects when the bundled script is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read Hermes shared memory files and write WorkBuddy strategy, effect, feedback, and evolution.db entries.]

## Skill Version(s):

4.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
