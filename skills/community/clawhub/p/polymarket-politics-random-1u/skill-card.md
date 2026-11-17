## Description:

Build and run a Polymarket politics-market trading skill with the AION SDK that searches active political markets on Polymarket, randomly chooses one market, and places a 1 USD trade through Aionmarket using an API key and optionally a wallet private key for self-custody live trading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fivegive249-ship-it](https://clawhub.ai/user/fivegive249-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill as an AION SDK template for finding active Polymarket politics markets and preparing a random 1 USD trade that remains dry-run unless live execution is explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit recurring real-money trades if live execution is enabled, especially when scheduled.

Mitigation: Keep dry-run mode for normal use, avoid RUN_LIVE for scheduled runs, and set strict external account limits before any live testing.

Risk: The artifact requests sensitive wallet access for optional self-custody live trading.

Mitigation: Do not provide a raw wallet private key unless the operator fully understands the custody model; prefer managed wallet setup or tightly limited accounts.

Risk: The random-entry strategy has weak trading limits and is not a production-quality decision process.

Mitigation: Review selected markets before live execution and add explicit sizing, filter, and risk checks before adapting the template for ongoing trading.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runnable script prints a Python dictionary containing the selected market, warnings, proposed trade, and dry-run or submitted status.]

## Skill Version(s):

1.0.0 (source: artifact metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
