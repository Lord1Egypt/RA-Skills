## Description: <br>
Comprehensive Interactive Brokers (IBKR) TWS/Gateway skill using ib_insync. Includes Python and bash CLIs for account, market data, historical data, contract lookup, scanners, and order lifecycle management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oscraters](https://clawhub.ai/user/oscraters) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading-operations users use this skill to run Interactive Brokers TWS or Gateway workflows from Python and bash CLIs, including account views, market data, contract lookup, scanners, and order lifecycle commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live brokerage orders without clear built-in confirmation or dry-run safeguards. <br>
Mitigation: Prefer paper trading first, verify the IBKR account and port before use, and add confirmation, size limits, and a dry-run workflow before allowing automated order-placement commands. <br>


## Reference(s): <br>
- [Interactive Brokers API Reference](references/api_reference.md) <br>
- [IBKR Campus API Hub](https://ibkrcampus.com/campus/ibkr-api-page/) <br>
- [TWS API Documentation](https://ibkrcampus.com/campus/ibkr-api-page/twsapi-doc/) <br>
- [ib_insync Documentation](https://ib-insync.readthedocs.io/) <br>
- [ClawHub Skill Page](https://clawhub.ai/oscraters/ibkr) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output with optional JSON and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return non-zero exit codes for dependency, connection, contract qualification, argument, and cancellation failures.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
