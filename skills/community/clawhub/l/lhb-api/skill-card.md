## Description: <br>
Provides agent-facing guidance and a Python client for querying A-share Dragon-Tiger List, stock pool, money-flow, account quota, and related market data APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fffy520](https://clawhub.ai/user/fffy520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and trading-research agents use this skill to call A-share market data endpoints for Dragon-Tiger List entries, brokerage-seat details, stock pools, and money-flow signals. The skill is suited for building market-monitoring workflows, research factors, and portfolio risk reference checks that require structured API responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market data can be stale, incomplete, or unsuitable as the sole basis for trading decisions. <br>
Mitigation: Confirm data freshness, exchange disclosures, and downstream calculations before using outputs in trading, risk, or compliance workflows. <br>
Risk: API usage can exceed documented daily quota or per-key frequency limits. <br>
Mitigation: Add request throttling, cache repeated parameter sets, and check account quota before high-volume agent runs. <br>
Risk: The bundled client calls an external HTTP API and returns remote data to the agent. <br>
Mitigation: Run the client only in environments where outbound access to the configured API host is approved, and avoid logging sensitive account or credential material. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/fffy520/lhb-api) <br>
- [Publisher profile](https://clawhub.ai/user/fffy520) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with HTTP examples and Python client code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured API usage instructions and JSON-returning Python client calls; API access is subject to documented quota and rate limits.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
