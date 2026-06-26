## Description: <br>
Public market data for crypto spot prices, FX rates, order books, and macro indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover Pilot Protocol finance service agents and request read-only public market data such as crypto prices, FX rates, order books, and market snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may send private portfolio, brokerage, credential, or account data to public finance service agents. <br>
Mitigation: Use the skill only for public market data queries and do not include private account, credential, brokerage, or portfolio information. <br>
Risk: Documented exclusions for SEC and macroeconomic data do not fully align with the listed finance agents. <br>
Mitigation: Treat SEC and macroeconomic entries as ambiguous until the publisher aligns the exclusions with the listed agents. <br>
Risk: The skill depends on Pilot Protocol, pilotctl, a running daemon, network 9 membership, and reachable service agents. <br>
Mitigation: Verify the Pilot Protocol setup and inspect each agent's /help contract before relying on returned data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-service-agents-finance) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot Skills Index](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Text] <br>
**Output Format:** [Markdown with bash command examples and JSON response envelopes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public market data responses are retrieved asynchronously through pilotctl inbox entries; summary commands return prose.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
