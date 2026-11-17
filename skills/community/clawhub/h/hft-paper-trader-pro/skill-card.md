## Description:

HFT Paper Trader Pro helps agents run crypto paper-trading simulations with multi-indicator technical analysis, dual-regime filtering, Kelly-style position sizing, stop-loss controls, journaling, and observation logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent simulate crypto paper trades, evaluate technical-analysis signals, manage a paper portfolio, and record trade outcomes for review. It is intended for simulation and strategy testing, not execution with real exchange credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide automated paper-trading activity that may be mistaken for real trading.

Mitigation: Confirm that no real exchange credentials or live order-routing tools are connected before using broad trading prompts.

Risk: The skill describes writing local paper-trading state to portfolio.json, journal.json, and observations.md.

Mitigation: Decide the target workspace and review proposed file writes before allowing the agent to update paper-trading state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/hft-paper-trader-pro)
- [Zero2Ai publisher profile](https://clawhub.ai/user/zero2ai-hub)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with prompts, code snippets, and suggested local state-file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose updates to portfolio.json, journal.json, and observations.md during paper-trading workflows.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
