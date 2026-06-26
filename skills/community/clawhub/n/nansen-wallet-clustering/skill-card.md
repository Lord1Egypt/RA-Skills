## Description: <br>
Cluster and attribute related wallets across funding chains, shared signers, CEX deposit patterns, governance voters, and related address groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and investigators use this skill to guide Nansen CLI wallet-attribution workflows, compare related addresses, expand candidate clusters with human confirmation, and report confidence-scored ownership signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses, chain selections, and investigation patterns are sent to Nansen through the CLI. <br>
Mitigation: Install only if the nansen-cli package and Nansen API usage are trusted, and avoid submitting sensitive addresses unless that disclosure is acceptable. <br>
Risk: Trace, batch, and L2 expansion commands can consume API credits or broaden the investigation beyond the seed wallet. <br>
Mitigation: Keep trace width at or below the documented limit, reserve counterparty expansion for the seed unless approved, and ask for human confirmation before querying newly found addresses. <br>


## Reference(s): <br>
- [Wallet Attribution Reference](artifact/REFERENCE.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/nansen-devops/nansen-wallet-clustering) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and confidence-scored attribution output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the nansen CLI and NANSEN_API_KEY; outputs address, owner, confidence, signals, and role when following the reference format.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
