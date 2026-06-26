## Description: <br>
Secure credential exchange with auto-expiry for Pilot Protocol agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to exchange API keys, tokens, and credentials between Pilot Protocol agents with expiration metadata and cleanup commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential-sharing examples handle secrets in plaintext and retain received credentials locally despite advertised expiry and security claims. <br>
Mitigation: Review before installing; use trusted recipients, short-lived least-privilege credentials, hardened temporary-file handling, secret-log prevention, and a real secret store or immediate deletion instead of local plaintext retention. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-keychain) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilot-protocol, pilotctl, jq, and openssl; examples create credential JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
