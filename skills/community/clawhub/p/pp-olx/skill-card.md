## Description: <br>
Printing Press CLI for Olx. OLX.pl job-listings reverse-engineered API (public, no auth) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[czarek-commits](https://clawhub.ai/user/czarek-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install and invoke olx-pp-cli for public OLX.pl job-listing data without authentication. It supports command discovery, agent-mode JSON output, setup checks, and optional MCP registration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external olx-pp-cli installer and binary. <br>
Mitigation: Install only when you trust the installer, verify olx-pp-cli --version, and run olx-pp-cli doctor before using live commands. <br>
Risk: Webhook delivery can send command output to a configured URL. <br>
Mitigation: Use webhook delivery only with URLs you chose and trust; otherwise keep output on stdout or a local file. <br>
Risk: Feedback entries and named profiles can retain local notes or repeated flag values. <br>
Mitigation: Review local feedback and saved profiles if you do not want agent notes or profile values retained. <br>


## Reference(s): <br>
- [Pp Olx on ClawHub](https://clawhub.ai/czarek-commits/pp-olx) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the olx-pp-cli binary; no authentication is required. Agent mode uses compact JSON output and non-interactive flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
