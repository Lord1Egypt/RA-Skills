## Description: <br>
Query package and express tracking worldwide through a unified API that integrates with Kdniao and can be extended to other courier providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlang-cn](https://clawhub.ai/user/openlang-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to track parcels by courier code and tracking number, or to add courier tracking through a reusable Python package and CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package tracking numbers, carrier identifiers, and limited verification data such as the last four digits of a phone number may be sent to Kdniao. <br>
Mitigation: Use only when users accept the external API requirement, disclose the data sent, and avoid providing verification data unless the carrier requires it. <br>
Risk: Kdniao API credentials are required for live queries and could be exposed if stored or committed carelessly. <br>
Mitigation: Keep credentials in local configuration, restrict access to the config file, and do not commit populated API keys. <br>


## Reference(s): <br>
- [ClawHub Package Track page](https://clawhub.ai/openlang-cn/package-track) <br>
- [Project homepage](https://github.com/openlang-cn/package-tracker.git) <br>
- [Kdniao instant tracking API documentation](https://www.kdniao.com/api-track) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [Human-readable tracking summaries, raw JSON responses, Python snippets, shell commands, and JSON configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI output may include shipment state and tracking traces; raw JSON mode returns the provider response.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
