## Description: <br>
Pg Setup helps agents install the ProxyGate CLI, configure API-key or wallet authentication, and verify access to the ProxyGate gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jwelten](https://clawhub.ai/user/jwelten) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill for first-time ProxyGate setup: installing the CLI, authenticating with an API key or wallet keypair, browsing available APIs, and making an initial gateway request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ProxyGate setup can involve API keys and wallet keypair files. <br>
Mitigation: Avoid sharing real API keys in chats or shared terminals, use dedicated keys where possible, and protect wallet keypair files with local file permissions and secure storage. <br>
Risk: ProxyGate wallet, listing deletion, tunnel, development forwarding, job, and skill-install commands can spend funds, expose services, delete resources, or install additional skills. <br>
Mitigation: Run those commands only after explicit user approval, review the exact command and target first, and use dry-run modes when available. <br>
Risk: The release depends on the @proxygate/cli package for setup actions. <br>
Mitigation: Verify the package source and installed version before using it for authenticated ProxyGate operations. <br>


## Reference(s): <br>
- [ProxyGate CLI Command Reference](references/commands.md) <br>
- [ProxyGate API Keys](https://app.proxygate.ai/keys) <br>
- [ProxyGate Gateway Docs](https://gateway.proxygate.ai/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI installation, authentication, verification, and troubleshooting steps.] <br>

## Skill Version(s): <br>
0.2.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
