## Description:

Finds Polymarket prediction-market pricing discrepancies, monitors opportunities, and outputs arbitrage summaries for paper trading or manual review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to scan Polymarket markets, detect math arbitrage candidates, monitor recurring scans, and review JSON results before any manual trading decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The monitor script can execute shell-injected commands through user-controlled paths or parameters.

Mitigation: Run only in a constrained environment, use trusted fixed paths, and fix command execution before routine use.

Risk: Webhook tokens can be exposed through command-line arguments or logs.

Mitigation: Avoid real webhook tokens on the command line; use a secret store or environment variable and redact logs.

Risk: Unpinned dependencies can change runtime behavior over time.

Mitigation: Use a fixed virtual environment with pinned versions for requests and beautifulsoup4.

Risk: Market prices shown by the homepage can be stale or non-executable, and liquidity can make detected arbitrage unavailable.

Mitigation: Paper trade first, manually verify prices and liquidity on Polymarket, and keep strict position limits before any real-money trading.

## Reference(s):

- [Polymarket](https://polymarket.com)
- [Polymarket Documentation](https://docs.polymarket.com)
- [Arbitrage Types](references/arbitrage_types.md)
- [Getting Started](references/getting_started.md)
- [ClawHub Skill Page](https://clawhub.ai/guohongbin-git/skills/polymarket-arbitrage-cn)
- [ClawHub Publisher Profile](https://clawhub.ai/user/guohongbin-git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces market scans and arbitrage result files under polymarket_data/ when scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
