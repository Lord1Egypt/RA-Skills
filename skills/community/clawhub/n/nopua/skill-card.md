## Description:

NoPUA coaches agents to recover from repeated failures with evidence-driven investigation, verification, proactive next steps, and responsible handoffs instead of fear-based pressure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuji-labs](https://clawhub.ai/user/wuji-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use NoPUA to guide an assistant after repeated failures, loops, unsupported guesses, or premature handoffs. The skill helps the agent investigate with tools, verify assumptions, change approach, and report boundaries responsibly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has intentionally broad behavioral scope and can encourage extra persistence on sensitive tasks.

Mitigation: Keep explicit confirmation requirements for production operations, account changes, legal, medical, financial, and destructive actions.

Risk: The skill encourages agents to investigate and verify more thoroughly, which can still produce incorrect or misleading guidance if results are not reviewed.

Mitigation: Review agent proposals and scanner results before deployment or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuji-labs/skills/nopua)
- [Project homepage](https://github.com/wuji-labs/nopua)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with checklists, diagnostic prompts, and structured handoff/report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown-only coaching guide with no hidden code, persistence, or exfiltration behavior according to ClawHub security evidence.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
