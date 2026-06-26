## Description: <br>
Control and query Hive Home (UK) smart heating, hot water, lights and devices via the unofficial API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m0nkmaster](https://clawhub.ai/user/m0nkmaster) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Hive Home users and automation developers use this skill to let an agent inspect and control Hive heating, hot water, lights, and related devices. It is intended for agent-assisted smart-home operations where the user supplies Hive credentials through environment variables or a trusted secret store. <br>

### Deployment Geography for Use: <br>
United Kingdom <br>

## Known Risks and Mitigations: <br>
Risk: Hive account credentials and device keys are sensitive secrets required for the skill to operate. <br>
Mitigation: Store HIVE_USERNAME, HIVE_PASSWORD, and HIVE_DEVICE_* values in a trusted secret store or agent configuration, and do not paste them into chat or commit them to source control. <br>
Risk: The skill can change heating, hot water, zone, boost, and mode settings on real Hive devices. <br>
Mitigation: Review the proposed command, target device or zone, temperature, duration, and mode before execution. <br>
Risk: First-time login may require SMS 2FA, and non-interactive runs need stored device credentials. <br>
Mitigation: Complete the first interactive login separately, then store the resulting device credentials securely for later agent runs. <br>


## Reference(s): <br>
- [Hive Home skill reference](references/REFERENCE.md) <br>
- [Hive credentials guide](references/CREDENTIALS.md) <br>
- [ClawHub Hive Home skill page](https://clawhub.ai/m0nkmaster/hivehome) <br>
- [Hive Home](https://www.hivehome.com) <br>
- [Pyhiveapi](https://github.com/Pyhass/Pyhiveapi) <br>
- [Pyhiveapi session examples](https://pyhass.github.io/pyhiveapi.docs/docs/examples/session/) <br>
- [Home Assistant Hive integration](https://www.home-assistant.io/integrations/hive/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run bundled Python commands that require Hive credentials, device keys for non-interactive use, and network access to Hive services.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
