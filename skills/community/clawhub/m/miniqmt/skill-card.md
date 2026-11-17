## Description:

miniQMT helps agents provide Python guidance for market data access and programmatic trading through the xtquant SDK and a logged-in miniQMT brokerage terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderwpf](https://clawhub.ai/user/coderwpf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quantitative trading users, and external agent users use this skill to configure xtquant, retrieve miniQMT market data, and draft Python examples for broker-connected trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes copy-ready examples for live trading, order cancellation, transfers, and bank-balance workflows.

Mitigation: Require explicit human confirmation, paper-trading checks, and position or transfer limits before running generated examples against a real account.

Risk: The skill expects access to a logged-in miniQMT brokerage terminal and account-specific paths or identifiers.

Mitigation: Keep credentials and account identifiers out of prompts and committed files, and run examples only in the intended brokerage environment.

Risk: The security summary notes insufficient safety controls and confirmation guidance for financial operations.

Mitigation: Add dependency pinning, error handling, and account-level safeguards before using the skill for production trading workflows.

## Reference(s):

- [ClawHub miniQMT Skill Page](https://clawhub.ai/coderwpf/skills/miniqmt)
- [XtQuant Native API Documentation](http://dict.thinktrader.net/nativeApi/start_now.html)
- [miniQMT xtdata Usage Guide](http://dict.thinktrader.net/nativeApi/xtdata.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include examples that call xtquant against a logged-in miniQMT terminal.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact files report 1.2.0 and 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
