## Description: <br>
A reusable operator-guided workflow improvement skill for OpenClaw and ClawLite that turns repeated failures into logged learnings, binary eval loops, SOPs, checklists, and proof-based operational improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and multi-agent workflow teams use this skill to capture repeated failures, run lightweight eval loops on guardrails, generate scorecards or recovery tickets, and promote reviewed improvements into local operating rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Promotion can append operational guidance to AGENTS.md, TOOLS.md, or SOUL.md. <br>
Mitigation: Review promotion targets first and use scripts/promote-learning.mjs with --dry-run before writing. <br>
Risk: Misconfigured WORKSPACE or OBSIDIAN_LEARNINGS_DIR values can direct local writes to unintended paths. <br>
Mitigation: Confirm both environment variables point only to locations the operator intends to modify. <br>
Risk: Captured lessons or promoted rules can preserve incorrect guidance if accepted without review. <br>
Mitigation: Review generated text before appending it to operating-rule files or an Obsidian vault. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/x-rayluan/openclaw-self-improvement) <br>
- [Learning Schema](references/schema.md) <br>
- [Promotion Guide](references/promotion-guide.md) <br>
- [Eval Loop](references/eval-loop.md) <br>
- [Decision Rules](references/decision-rules.md) <br>
- [Examples](references/examples.md) <br>
- [ClawLite](https://clawlite.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown entries, local files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-file workflow; promotion writes should be reviewed and can be previewed with --dry-run.] <br>

## Skill Version(s): <br>
0.2.11 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
