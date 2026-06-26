## Description: <br>
Controls Xiaomi Home devices over a local network with miiocli, including status checks, power toggles, and MIOT property changes for smart plugs, humidifiers, and rice cookers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiqiezhenxi](https://clawhub.ai/user/yiqiezhenxi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and home automation users can use this skill to translate natural-language Xiaomi Home requests into local miiocli commands for device status, power, and property control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Xiaomi local control tokens and may expose them through chats, logs, markdown, or version control. <br>
Mitigation: Keep tokens out of shared outputs and repositories, redact them from logs, and inspect any token extractor before running it. <br>
Risk: The skill can change real appliance state, including power and MIOT properties. <br>
Mitigation: Require explicit user confirmation before executing commands that change device power or appliance state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yiqiezhenxi/home-xiaomi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require miiocli plus user-provided Xiaomi device IP addresses and local control tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
