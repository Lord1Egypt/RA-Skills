## Description: <br>
Publishes locally running apps as peer-to-peer URLs that anyone with the link can open in a browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phact](https://clawhub.ai/user/phact) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use P2claw to share a local web app or dev server with another person or device by exposing a confirmed localhost port as a public peer-to-peer URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A shared P2claw URL can make a local app reachable from the public internet by anyone with the link. <br>
Mitigation: Confirm the exact app and port with the user before exposing it, explain that the URL is public, and remove the route when sharing is finished. <br>
Risk: Debug, admin, unauthenticated, credentialed, or tool-enabled local services can expose sensitive capabilities when published. <br>
Mitigation: Avoid exposing those services unless access controls are verified; for private sharing, use a tunnel with authentication or another protected sharing method. <br>
Risk: Installing the helper binary requires trusting the P2claw release source. <br>
Mitigation: Use the bundled installer, rely on its SHA-256 verification when checksums are published, and install only from a trusted release source. <br>


## Reference(s): <br>
- [P2claw ClawHub listing](https://clawhub.ai/phact/p2claw) <br>
- [P2claw install endpoint](https://p2claw.com/install) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public share URLs, QR-code output, route names, daemon status checks, and cleanup commands.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
