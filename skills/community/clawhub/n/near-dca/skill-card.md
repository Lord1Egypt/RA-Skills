## Description: <br>
Dollar-cost averaging for NEAR tokens with flexible scheduling, performance tracking, and cancellation support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaiss](https://clawhub.ai/user/shaiss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and NEAR users use this skill to create, manage, pause, resume, and inspect recurring NEAR dollar-cost averaging strategies. It also supports execution history, cost-basis calculation, and alert configuration for DCA workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles wallet credentials and recurring purchase automation. <br>
Mitigation: Review the code before installation and use secure credential storage; do not use a funded wallet private key unless the implementation has been independently verified. <br>
Risk: Transaction hashes, prices, alerts, and performance data may be simulated or untrusted until real integrations are verified. <br>
Mitigation: Validate on-chain execution, price sources, and notification delivery before relying on the skill for trading decisions. <br>
Risk: Recurring purchases can create financial exposure if schedules or strategy parameters are incorrect. <br>
Mitigation: Start with limited amounts, review scheduled strategies regularly, and confirm pause, resume, and cancellation behavior before unattended use. <br>


## Reference(s): <br>
- [NEAR DeFi](https://near.org/defi/) <br>
- [Ref Finance](https://ref.finance/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Action responses, JSON data, and command-line text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist DCA strategy state and execution history in local JSON storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, skill.yaml, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
