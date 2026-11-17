## Description:

A reusable operator-guided workflow improvement skill for OpenClaw and ClawLite that turns repeated failures into logged learnings, binary eval loops, SOPs, checklists, and proof-based operational improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent teams use this skill to capture repeated workflow failures, run binary eval loops on proposed guardrails, and promote reviewed improvements into local operating rules and notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Promotion can append arbitrary text to persistent agent instruction files such as AGENTS.md, TOOLS.md, and SOUL.md.

Mitigation: Treat promotion as a privileged policy change and use dry-run output plus manual diff review before accepting writes.

Risk: Repair-ticket and Obsidian writes can be affected by insufficient path controls or untrusted path-like inputs.

Mitigation: Run only with trusted WORKSPACE, OBSIDIAN_LEARNINGS_DIR, progress reports, dates, and ticket directories.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/x-rayluan/skills/openclaw-self-improvement)
- [ClawLite](https://clawlite.ai)
- [Learning Schema](references/schema.md)
- [Promotion Guide](references/promotion-guide.md)
- [Eval Loop for Self-Improvement](references/eval-loop.md)
- [Practical Examples for Self-Improvement Eval Loops](references/examples.md)
- [Decision Rules for Self-Improvement](references/decision-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, local file updates, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and trusted WORKSPACE and OBSIDIAN_LEARNINGS_DIR values; writes are local file operations.]

## Skill Version(s):

0.2.11 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
