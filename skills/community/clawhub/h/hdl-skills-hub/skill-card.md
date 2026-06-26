## Description: <br>
HDL Skills Hub coordinates HDL-MCP-Server skills for authentication, request signing, product lookup, cart operations, home management, and smart-home device control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superzhangquansong](https://clawhub.ai/user/superzhangquansong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to navigate HDL account authentication, signed HDL API requests, product and shopping-cart workflows, home selection, and smart-home device status or control tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require agents to handle HDL account credentials, local app secrets, access tokens, refresh tokens, and request signatures. <br>
Mitigation: Install only from a trusted publisher, prefer platform-managed secrets, and avoid exposing credentials, tokens, signatures, or IDs in agent responses or logs. <br>
Risk: The skill can change physical smart-home device state, including lights, curtains, and other connected devices. <br>
Mitigation: Require clear confirmation of the target home, room, device, and action before executing device-control operations. <br>
Risk: The security scan reports insufficient scoping and confirmation safeguards for smart-home actions. <br>
Mitigation: Use versions or deployment policies that scope account access, confirm destructive or physical-state-changing requests, and warn before transmitting passwords or changing device state. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/superzhangquansong/hdl-skills-hub) <br>
- [HDL device list API endpoint](https://gateway.hdlcontrol.com/home-wisdom/app/device/list) <br>
- [HDL device control API endpoint](https://gateway.hdlcontrol.com/home-wisdom/app/device/control) <br>
- [HDL home list API endpoint](https://gateway.hdlcontrol.com/home-wisdom/app/home/list) <br>
- [HDL login API endpoint](https://gateway.hdlcontrol.com/basis-footstone/user/oauth/login) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and structured API workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may involve HDL account credentials, tokens, signatures, home identifiers, device identifiers, and physical smart-home state changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
