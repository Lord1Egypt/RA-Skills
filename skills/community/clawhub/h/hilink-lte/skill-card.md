## Description: <br>
Control Huawei HiLink USB LTE modems via their local REST API to send and read SMS, check signal and status, manage SIM PIN state, query prepaid balance, and inspect connection information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[And0r-](https://clawhub.ai/user/And0r-) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators managing local Huawei HiLink USB LTE modems use this skill to configure connectivity and run modem tasks such as SMS, signal checks, SIM PIN handling, USSD balance queries, and device status inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send or delete SMS and run USSD requests through a local HiLink modem. <br>
Mitigation: Review the target number, message body, SMS index, and USSD operation before allowing SMS send, SMS delete, or balance commands to run. <br>
Risk: A saved SIM PIN in the HiLink config could unlock modem access if the config file is exposed. <br>
Mitigation: Avoid storing HILINK_PIN unless unattended unlock is required, and restrict ~/.config/hilink/config so only the intended user can read it. <br>
Risk: The helper can use sudo network commands and alter the LTE interface state. <br>
Mitigation: Review sudo network actions before execution and keep the LTE interface configured without a default route or DNS that could override the main network. <br>


## Reference(s): <br>
- [HiLink API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/And0r-/hilink-lte) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that interact with a local modem and network interface.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
