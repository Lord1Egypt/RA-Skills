## Description: <br>
Connect an MCP-compatible agent to Polar AccessLink training, sleep, Nightly Recharge, PPI/HRV, route, and sample data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install, configure, verify, and troubleshoot Polar MCP for MCP-compatible clients while keeping OAuth tokens and private Polar data protected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Polar OAuth tokens and fitness, sleep, HRV, sample, or route/GPS data are sensitive. <br>
Mitigation: Keep local token files private, do not print secrets or private user data, and revoke Polar access when the connection is no longer needed. <br>
Risk: Authenticated agent access may expose health or location data through MCP surfaces. <br>
Mitigation: Use connection status, manifest, doctor, privacy audit, or dry-run checks first, and keep route/GPS access opt-in with explicit user consent. <br>
Risk: Setup relies on a third-party npm package and linked project. <br>
Mitigation: Install only if the publisher, package, and linked project are trusted for the user's environment. <br>


## Reference(s): <br>
- [Polar MCP repository](https://github.com/davidmosiah/polarmcp) <br>
- [Polar connector documentation](https://wellness.delx.ai/connectors/polar) <br>
- [ClawHub release page](https://clawhub.ai/davidmosiah/polar-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include setup, OAuth, privacy-audit, dry-run, and troubleshooting guidance for MCP-compatible clients.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
