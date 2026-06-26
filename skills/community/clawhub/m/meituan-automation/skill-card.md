## Description: <br>
Meituan Physical Automation lets an agent operate a trusted Android phone through ADB and UIAutomator2 to search restaurants, add food items in Meituan, and stop at checkout for user review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oscarka](https://clawhub.ai/user/oscarka) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate a trusted Android phone running Meituan for food-ordering workflows, from restaurant search through checkout review. The user must supervise the device and complete any payment or verification manually. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes broad Android phone control and can read sensitive screen or address information. <br>
Mitigation: Run it only on a trusted machine and device, supervise every run, and disable USB debugging or stop the service after use. <br>
Risk: The HTTP control surface and automation commands can change cart state or navigate toward checkout. <br>
Mitigation: Do not expose the server to a network; bind to localhost with authentication where possible and require explicit user confirmation before cart changes or checkout navigation. <br>
Risk: The package includes Frida-related dependencies and unpinned dependency ranges. <br>
Mitigation: Review whether Frida is necessary, remove it if unused, and pin dependencies before installing in a sensitive environment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/oscarka/meituan-automation) <br>
- [Meituan official site](https://www.meituan.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON CLI or HTTP responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow returns readable status, screen, cart, address, and checkout information; it should stop before payment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
