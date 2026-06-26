## Description: <br>
Query Nasdaq public market APIs from scripts or agent workflows for stock screener pulls, symbol lists, pagination over screener rows, and guidance on official Nasdaq Data Link public API docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oscraters](https://clawhub.ai/user/oscraters) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to fetch public Nasdaq stock screener rows or ticker symbols with deterministic pagination, then ground API selection, authentication, and rate-limit decisions in Nasdaq documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Bash CLI makes external requests to Nasdaq public endpoints. <br>
Mitigation: Review the script before execution and use sensible pagination, timeout, and rate-limit settings. <br>
Risk: The public screener endpoint behavior or response schema may change. <br>
Mitigation: Validate the expected data.rows response shape before downstream processing and fail fast on unexpected status messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oscraters/nasdaq-public) <br>
- [Nasdaq API References](references/api_docs.md) <br>
- [Nasdaq Data Organization](https://docs.data.nasdaq.com/docs/data-organization) <br>
- [Nasdaq real-time/delayed REST API rate limits](https://docs.data.nasdaq.com/docs/rate-limits-for-real-timedelayed-rest-api) <br>
- [Nasdaq Data Link API overview](https://www.nasdaq.com/solutions/data/nasdaq-data-link/api) <br>
- [Nasdaq public screener endpoint](https://api.nasdaq.com/api/screener/stocks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON or symbol-list command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled CLI supports limit, offset, exchange, tableonly, download, format, timeout, and print-url options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
