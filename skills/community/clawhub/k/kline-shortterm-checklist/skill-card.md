## Description:

Provides an A-share short-term stock screening checklist that combines K-line pattern review, the 96 principle, 2:30 p.m. screening rules, market-data helper scripts, and optional Wind-backed announcement and intraday checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handm-735](https://clawhub.ai/user/handm-735)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts can use this skill to apply a repeatable technical-analysis checklist before evaluating A-share short-term candidates or an individual stock's buy, hold, and risk conditions. It is a screening and reporting aid, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional local workbench has unauthenticated rerun controls and reads or writes files in the working directory.

Mitigation: Run the workbench only on localhost, keep it stopped when not in active use, and do not expose it through a proxy, tunnel, or LAN share.

Risk: The security evidence reports unsafe HTML rendering and weakened market-data TLS handling.

Mitigation: Treat generated reports and fetched market data as untrusted, review outputs before acting on them, and prefer deployment only after HTML escaping and TLS verification issues are fixed.

Risk: The skill supports financial screening workflows that can produce misleading or stale conclusions if market data, announcement checks, or manual chart review are incomplete.

Mitigation: Use results as decision-support only, verify material facts with authoritative sources, and apply independent risk, position-sizing, and stop-loss controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/handm-735/skills/kline-shortterm-checklist)
- [K-line short-term checklist reference](references/checklist.md)
- [K-line pattern reference](references/kline_patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, JSON intermediate files, and HTML screening reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write candidates.json, screen_meta.json, kline_data.json, announcement_plan.json, announcement_check.json, intraday_plan.json, intraday_raw.json, intraday_strength.json, and fixed-format HTML reports in the working directory.]

## Skill Version(s):

1.0.5 (source: server release evidence; artifact frontmatter lists 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
