## Description: <br>
Blocknative helps agents query Blocknative gas and chain data through the OOMOL connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they want an agent to retrieve Blocknative Ethereum gas-price estimates, gas-price distributions, gas-oracle metadata, and supported chain information through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connecting Blocknative through OOMOL grants OOMOL access to an API-key-backed service. <br>
Mitigation: Connect Blocknative only from an authorized OOMOL account and only when that service access is acceptable for the deployment. <br>
Risk: The optional oo CLI installation path can execute a remote installer command. <br>
Mitigation: Review the install command or use the documented install guide before running it in the target environment. <br>
Risk: The skill depends on live OOMOL authentication, connection state, and billing status. <br>
Mitigation: Run setup, reconnection, or billing steps only when the oo CLI reports the matching authentication, connection, or credit error. <br>


## Reference(s): <br>
- [Blocknative Homepage](https://www.blocknative.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run oo CLI connector schema and read-only connector actions that return JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: skill metadata and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
