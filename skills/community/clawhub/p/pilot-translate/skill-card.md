## Description: <br>
Auto-translate messages between agents using different languages over the Pilot Protocol network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure cross-language communication between agents on the Pilot Protocol network when collaborators use different languages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent messages may be sent through third-party translation tools, including sensitive customer data or personal information. <br>
Mitigation: Use only organization-approved translation backends, avoid translating secrets or regulated content, and prefer self-hosted or enterprise-approved translation for sensitive messages. <br>
Risk: The install snippet uses a shortened URL and sudo move command for an external translation tool. <br>
Mitigation: Independently verify translation tool sources before installation and avoid privileged installation commands unless the source is trusted. <br>
Risk: Translated messages may be sent to unintended Pilot recipients. <br>
Mitigation: Confirm recipient hostnames before sending and disable auto-translation when it is no longer needed. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-translate) <br>
- [Publisher profile](https://clawhub.ai/user/teoslayer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl on PATH, a running Pilot Protocol daemon, and an external translation tool.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
