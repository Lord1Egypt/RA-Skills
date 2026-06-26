## Description: <br>
Control Apple HomeKit smart home devices. Supports listing, discovering, pairing devices, and controlling lights, switches, outlets, thermostats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manifoldor](https://clawhub.ai/user/manifoldor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and smart-home users use this skill to discover, pair, list, and control local Apple HomeKit accessories from an agent-assisted Python workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control paired HomeKit accessories, including unpairing devices and batch power changes. <br>
Mitigation: Review commands before running them and confirm the target alias, action, and scope before executing state-changing operations. <br>
Risk: The local HomeKit pairing file grants access to paired accessories if exposed. <br>
Mitigation: Protect the local pairing file and avoid sharing or committing HomeKit configuration data. <br>
Risk: Python dependency drift could change HomeKit control behavior or introduce dependency risk. <br>
Mitigation: Use a virtual environment or pinned package versions for the HomeKit Python dependencies. <br>


## Reference(s): <br>
- [HomeKit API Reference](references/api.md) <br>
- [Apple HomeKit Documentation](https://developer.apple.com/homekit/) <br>
- [homekit_python Library Documentation](https://github.com/jlusiardi/homekit_python) <br>
- [ClawHub Skill Page](https://clawhub.ai/manifoldor/homekit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that discover, pair, unpair, inspect, or change HomeKit accessory state.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
