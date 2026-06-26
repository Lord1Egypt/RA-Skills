## Description: <br>
Searches the Tor dark web, fetches .onion hidden-service pages, rotates Tor identities, and supports structured multi-step OSINT investigations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JacobJandon](https://clawhub.ai/user/JacobJandon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security researchers, threat-intelligence teams, and incident responders use this skill to search Tor indexes, fetch hidden-service pages, monitor dark-web mentions, and generate structured OSINT reports for lawful investigations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for Tor, setup, and script execution authority while referenced executable scripts are not included in the artifact for review. <br>
Mitigation: Review the upstream OnionClaw code before running setup or operational scripts, and test changes in a controlled environment. <br>
Risk: Automatic setup and Tor configuration can change local service behavior. <br>
Mitigation: Use automatic setup only after reviewing the Tor service and torrc changes, or perform manual setup with least-privilege configuration. <br>
Risk: Reports and watch outputs may contain leaked credentials, PII, or internal company data. <br>
Mitigation: Write outputs to private access-controlled directories, avoid shared temporary paths, and clear or disable watch jobs when finished. <br>
Risk: LLM-assisted analysis may send sensitive investigation material to a remote provider. <br>
Mitigation: Do not submit leaked credentials, PII, or internal company data to a remote LLM without authorization; use local inference or redact sensitive content when required. <br>


## Reference(s): <br>
- [ClawHub OnionClaw listing](https://clawhub.ai/JacobJandon/onionclaw) <br>
- [OnionClaw repository](https://github.com/JacobJandon/OnionClaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, CSV, STIX, MISP, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional structured OSINT report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tor and Python dependencies; LLM-based analysis may require a configured provider.] <br>

## Skill Version(s): <br>
2.1.13 (source: server evidence release version and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
