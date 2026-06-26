## Description: <br>
OGP helps agents manage Open Gateway Protocol federation, peer communication, framework selection, and cross-gateway project collaboration across OpenClaw and Hermes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dp-pcs](https://clawhub.ai/user/dp-pcs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure OGP, connect with trusted peers, send federation messages, manage scopes, and troubleshoot OpenClaw or Hermes gateway state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates sensitive federation and agent access to the external @dp-pcs/ogp CLI. <br>
Mitigation: Review and pin the CLI version before installation, and protect OpenClaw tokens plus ~/.ogp* state files. <br>
Risk: Broad peer scopes or peer-state reset commands can expose capabilities or remove existing federation relationships. <br>
Mitigation: Only approve verified peers, customize granted scopes when possible, and run reset commands only for the exact framework files intentionally being changed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dp-pcs/ogp) <br>
- [OGP documentation](https://github.com/dp-pcs/ogp) <br>
- [Rendezvous discovery service](https://rendezvous.elelem.expert) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may modify OGP gateway configuration, peer relationships, and local OGP state files when executed by the user.] <br>

## Skill Version(s): <br>
0.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
