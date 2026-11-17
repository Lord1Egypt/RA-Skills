## Description:

Event Analyzer helps agents evaluate important market and policy events through structured evidence collection, signal filtering, source assessment, and market-impact analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to review significant events, separate durable signals from noise, assess source quality, and produce structured event-analysis reports. The skill is especially oriented toward Chinese-language business, market, policy, and trading-impact analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs may be mistaken for licensed financial advice because the skill can generate named instruments, position sizes, timing, and stop-loss levels.

Mitigation: Treat outputs as unlicensed market commentary, require independent human review, and do not use them as the sole basis for investment or trading decisions.

Risk: Requested tool permissions are broader than the stated research workflow justifies.

Mitigation: Install with tightly limited tools; allow WebSearch only when needed and block Exec and Message unless separately justified and approved.

Risk: Market, policy, and event data can become stale or be cited with unclear source quality.

Mitigation: Require current, traceable primary-source URLs for material claims and re-check data freshness before acting on time-sensitive conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lj22503/skills/lj22503-fanli-analyzer)
- [README](artifact/README.md)
- [Event analysis sample](artifact/examples/event-analysis-sample.md)
- [Weekly events example](artifact/examples/weekly-events-20260416.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured Chinese-language event research that may include market commentary, source-quality judgments, signal rankings, position sizing, timing, and stop-loss suggestions.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
