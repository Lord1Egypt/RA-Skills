## Description: <br>
Trade Polymarket BTC 5-minute and 15-minute fast markets using CEX price momentum signals via Simmer API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leogordon2004](https://clawhub.ai/user/leogordon2004) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to configure and run an agent-guided Polymarket fast-market trading workflow with dry-run checks, optional live execution, position monitoring, and configurable signal thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can automatically spend real USDC without a second confirmation or strong built-in loss limits. <br>
Mitigation: Start in dry-run, use small max-position settings, verify the publisher and version, and add external spend or loss limits before live use. <br>
Risk: Running live quiet mode from cron or heartbeat can repeat trades with little visible feedback. <br>
Mitigation: Avoid unattended live --quiet loops unless there is a clear stop mechanism, monitoring, and enforced budget limits. <br>
Risk: A custom SIMMER_API_BASE can send authenticated requests to an endpoint the user controls or trusts incorrectly. <br>
Mitigation: Leave SIMMER_API_BASE unset for the default Simmer endpoint unless the replacement endpoint has been explicitly verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leogordon2004/poly) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run is the default; live trading requires SIMMER_API_KEY and an explicit --live flag.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
