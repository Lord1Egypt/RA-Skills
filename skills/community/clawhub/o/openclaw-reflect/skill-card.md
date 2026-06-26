## Description: <br>
Self-improvement layer with evaluation separation, rollback, and tiered operator gates that observes outcomes across sessions, detects recurring patterns, proposes improvements, validates proposals through a separate evaluator invocation, and applies changes with snapshot and rollback capability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor recurring tool and workflow failures, propose targeted improvements to persistent agent memory or instructions, route proposals through a separate evaluator, and apply or queue changes according to blast-radius gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AtlasPA/openclaw-reflect) <br>
- [README](README.md) <br>
- [Agent payments](AGENT-PAYMENTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, JavaScript hook behavior, and JSON or JSONL state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Records local tool outcomes, can call external evaluator backends when configured, and may modify MEMORY.md or CLAUDE.md with rollback snapshots; review .reflect logs and proposed diffs before trusting applied changes.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
