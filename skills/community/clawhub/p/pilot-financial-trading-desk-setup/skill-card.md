## Description: <br>
Deploys a four-agent financial trading desk for coordinated market analysis, sentiment scanning, risk management, and trade execution workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a Pilot Protocol trading desk with analyst, sentiment, risk-manager, and executor agents. It helps install role-specific skills, set hostnames, establish trust handshakes, and define data flows for automated or semi-automated trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup can enable real trade execution through downstream Pilot skills. <br>
Mitigation: Use only paper-trading or sandbox exchange credentials until every downstream skill is reviewed and verified. <br>
Risk: Production exchange credentials could place trades without sufficient loss-prevention controls. <br>
Mitigation: Require explicit position limits, human approval gates, audit logging, and a quick disable path before connecting production keys. <br>
Risk: The executor role depends on pilot-webhook-bridge for exchange API integration. <br>
Mitigation: Review pilot-webhook-bridge and related downstream skills before allowing execution against real venues. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-financial-trading-desk-setup) <br>
- [Publisher Profile](https://clawhub.ai/user/teoslayer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with shell command examples and JSON manifest templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role-specific setup instructions, peer handshake guidance, and Pilot Protocol message examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
