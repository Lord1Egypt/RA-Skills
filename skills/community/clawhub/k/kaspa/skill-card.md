## Description: <br>
Simple self-custody CLI wallet for the Kaspa blockchain that helps agents check balances, send KAS, estimate fees, generate payment URIs, and return JSON for automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Manyfestation](https://clawhub.ai/user/Manyfestation) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation agents use this skill to manage a Kaspa CLI wallet, inspect network and balance state, estimate transaction fees, send KAS, and generate payment request URIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend cryptocurrency using wallet secrets in the agent environment. <br>
Mitigation: Use a testnet or low-balance wallet first, avoid placing a main wallet seed phrase or private key in a shared agent environment, and manually verify recipient, amount, fee, and network before every send. <br>
Risk: The installer uses a higher-risk dependency setup path, including an unpinned Kaspa dependency and a get-pip fallback. <br>
Mitigation: Review and pin the dependency before using real funds, and consider disabling the get-pip fallback in controlled environments. <br>


## Reference(s): <br>
- [Kaspa Docs](https://docs.kaspa.org/) <br>
- [Kaspa Explorer](https://explorer.kaspa.org/) <br>
- [kaspa-py SDK](https://github.com/aspect-build/kaspa-py) <br>
- [Skill README](README.md) <br>
- [Skill Documentation](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Wallet commands may read secrets from environment variables and may submit cryptocurrency transactions on the configured Kaspa network.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
