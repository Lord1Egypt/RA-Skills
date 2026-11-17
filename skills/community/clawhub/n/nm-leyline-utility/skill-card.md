## Description:

Scores agent actions by expected gain, cost, uncertainty, and redundancy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to decide when an agent should respond, retrieve information, call a tool, verify, delegate, or stop. It helps control cost and avoid redundant orchestration steps by applying a utility score before action selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence whether an agent uses tools or delegates work, so an unsuitable prescriptive configuration could cause the agent to skip useful action or over-follow heuristic scores.

Mitigation: Use the default advisory mode for normal adoption and enable prescriptive mode only where utility scoring is intentionally meant to constrain action selection.

Risk: The utility score depends on self-estimated gain, uncertainty, and redundancy, which can be inaccurate for ambiguous tasks.

Mitigation: Require the agent to log score breakdowns and rationale, then review high-impact decisions before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-utility)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with scoring formulas, checklists, and action report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory or opt-in prescriptive decision guidance; no executable code is included in the artifact.]

## Skill Version(s):

1.9.19 (source: server release metadata; artifact frontmatter lists 1.9.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
