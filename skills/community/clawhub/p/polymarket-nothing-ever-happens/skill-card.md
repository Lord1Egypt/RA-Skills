## Description:

Scans standalone non-sports yes/no Polymarket markets, filters for low-priced NO opportunities, checks fees and safeguards through Simmer, and can place configurable NO trades.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill as a Simmer-based example for scanning Polymarket markets, tuning a NO-price strategy, and reviewing candidate trades before optional execution. It is suited for paper trading or low-balance experimentation unless the security review findings are resolved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use financial credentials and wallet funds for prediction-market trading.

Mitigation: Use paper trading or a dedicated low-balance wallet, and do not provide production wallet keys or meaningful funds until the review findings are resolved.

Risk: The security review reports an account-changing redemption step even when modes are described as scan-only or dry-run.

Mitigation: Avoid scheduled runs and verify redemption behavior before enabling live execution.

Risk: The security guidance calls out dependency pinning and default-setting mismatch concerns.

Mitigation: Pin and review the exact Simmer SDK and gamma_api.py sources, and confirm runtime defaults before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simmer/skills/polymarket-nothing-ever-happens)
- [Strategy reference: sterlingcrispin/nothing-ever-happens](https://github.com/sterlingcrispin/nothing-ever-happens)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print candidate summaries, paper-trade status, live trade results, skip reasons, errors, and automaton status JSON.]

## Skill Version(s):

1.0.3 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
