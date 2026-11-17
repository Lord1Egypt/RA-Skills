## Description:

Pair NO-advance with YES-winner legs for the same 2026 World Cup team to trade cross-market mispricing.

This skill is for research and development only.

## Publisher:

[alyna123t](https://clawhub.ai/user/alyna123t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill to scan 2026 World Cup prediction markets, identify paired NO-advance and YES-winner opportunities for the same team, and optionally place orders through Simmer-supported venues after reviewing the risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live execution can place real-money trades that lose money.

Mitigation: Run dry-run or sim mode first and use --live only after explicit review and acceptance of trading risk.

Risk: The Simmer API key may grant account access for wallet, positions, and trading actions.

Mitigation: Use a restricted Simmer API key if available and review account status before and after live runs.

Risk: A failed second leg may leave an unhedged position.

Mitigation: Keep safeguards enabled, review fills after live runs, and reconcile exposure before placing additional pairs.

Risk: Local daily budget and cooldown files may not reflect partial or failed execution.

Mitigation: Check actual venue/account state after live attempts and do not rely only on local state files for exposure control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alyna123t/skills/polymarket-world-cup-delta-pairs)
- [Strategy source](https://x.com/zETHerka/status/2061162222156460540)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus command-line text and JSON configuration output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Simmer APIs and can place live prediction-market trades when run with --live.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
