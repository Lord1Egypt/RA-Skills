## Description:

Polymarket Place helps agents place real-money Polymarket CLOB V2 orders and requires companion stop-loss, trailing-stop, portfolio-risk, and exit controls after live fills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polyparlay](https://clawhub.ai/user/polyparlay)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route agent-assisted Polymarket order placement while requiring separate stop and portfolio-risk controls before positions are left unattended.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real-money Polymarket orders.

Mitigation: Install only when live trading is intended, require explicit approval for every order, and confirm that the operator understands the financial exposure.

Risk: The release evidence reports broad routing, required follow-on installs, version mismatches, and an unsafe launcher fallback.

Mitigation: Review the skill, companion skills, exact package versions, hashes, and launcher path before enabling the skill or arming watcher processes.

Risk: Polymarket positions do not have native stop controls in the supplied artifact description.

Mitigation: Use the required companion stop-loss, trailing-stop, portfolio-risk, exit, or agent-guard skills before leaving any live position unattended.

## Reference(s):

- [Polymarket Place ClawHub page](https://clawhub.ai/polyparlay/skills/polymarket-place)
- [polyparlay publisher profile](https://clawhub.ai/user/polyparlay)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to install companion risk-control skills and review package pins before use.]

## Skill Version(s):

1.0.13 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
