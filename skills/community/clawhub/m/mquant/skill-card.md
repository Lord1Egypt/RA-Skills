## Description:

Matic MQuant strategy development assistant that generates Python strategy code for the Matic-MQuant platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigbigjuanjuan](https://clawhub.ai/user/bigbigjuanjuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative trading users use this skill to draft, debug, and organize runnable Matic-MQuant Python strategies with platform-specific API references, logging conventions, and trading-rule checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated strategies and bundled examples may place real trades when loaded and run in Matic.

Mitigation: Review symbols, order logic, quantities, account type, and risk limits, then test in a Matic simulation or test environment before live use.

Risk: Matic-MQuant does not support backtesting, so strategy behavior may be unvalidated before execution.

Mitigation: Use the documented test environment workflow, logging requirements, and deployment checklist to validate behavior before using real capital.

Risk: The skill may create or clean up strategy versions and log files in a user-provided directory.

Mitigation: Use a dedicated writable strategy directory and review generated file names, retained versions, and cleanup behavior before running the workflow on important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bigbigjuanjuan/skills/mquant)
- [Publisher profile](https://clawhub.ai/user/bigbigjuanjuan)
- [artifact/SKILL.md](artifact/SKILL.md)
- [artifact/README.md](artifact/README.md)
- [artifact/reference/API_REFERENCE.md](artifact/reference/API_REFERENCE.md)
- [artifact/reference/LOG_FORMAT.md](artifact/reference/LOG_FORMAT.md)
- [artifact/reference/mquantFAQ.md](artifact/reference/mquantFAQ.md)
- [HTSC MQuant help](https://inst.htsc.com/helpOnline?productId=4&moduleCode=1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with Python code blocks, file paths, configuration steps, and optional generated .py and .log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated strategies are intended for review and testing in Matic-MQuant before live trading.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
