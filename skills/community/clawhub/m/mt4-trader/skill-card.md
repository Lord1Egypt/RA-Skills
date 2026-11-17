## Description:

MT4 Trader Bridge enables Python-to-MetaTrader 4 expert-advisor communication through local JSON files for market data, trading, order management, risk controls, alerts, and grid strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apuba](https://clawhub.ai/user/apuba)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-automation operators use this skill to connect an agent or Python scripts to MT4 for quotes, position review, order placement, stop-loss/take-profit changes, alerts, summaries, and grid strategy control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install unverified MT4 .ex4 expert-advisor binaries that can affect trading accounts.

Mitigation: Use only a demo or tightly limited account unless the binaries are independently trusted and verified; pin and hash-check any downloaded .ex4 files.

Risk: The bridge exposes high-impact live trading actions, including order placement, bulk close, stop changes, and grid strategy controls.

Mitigation: Require explicit confirmation for every trade or bulk-close action and do not enable live trading for unverified files.

Risk: The file-based bridge directory and summary webhook can be abused if untrusted local processes or endpoints are allowed.

Mitigation: Restrict the bridge directory to trusted local processes and use only HTTPS allowlisted webhook endpoints for summaries.

Risk: The artifact instructs users to enable DLL imports for MT4 expert advisors.

Mitigation: Do not enable DLL imports for unverified files.

## Reference(s):

- [MT4 Bridge API Reference](artifact/references/api_docs.md)
- [ClawHub Skill Page](https://clawhub.ai/apuba/skills/mt4-trader)
- [Gitee MT4 Download Page](https://gitee.com/3603317/skill-plugin/tree/master/mt4)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON bridge requests, position summaries, alert configurations, and webhook message payloads when scripts are run.]

## Skill Version(s):

1.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
