## Description: <br>
Interpret blockchain data strategically; identify patterns, anomalies, and flows with data-backed evidence and explicit uncertainty. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzfshark](https://clawhub.ai/user/mzfshark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze wallet, contract, and transaction activity, map fund flows, identify anomalies, and separate evidence-backed facts from hypotheses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may provide private keys, seed phrases, exchange credentials, signing access, or unnecessary financial context while requesting blockchain analysis. <br>
Mitigation: Provide only public addresses, transaction hashes, chain, timeframe, and relevant labels; do not provide private keys, seed phrases, exchange credentials, signing access, or unnecessary financial context. <br>
Risk: Analysis can be misleading if incomplete wallet, contract, transaction, chain, or timeframe data is treated as conclusive. <br>
Mitigation: State missing inputs explicitly, distinguish facts from hypotheses, include confidence levels, and identify what evidence would change each conclusion. <br>
Risk: Broad trigger phrases may activate the skill when a user did not intend to analyze sensitive blockchain activity. <br>
Mitigation: Narrow trigger phrases during deployment if accidental activation is a concern. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mzfshark/onchain-analysis) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mzfshark) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown with structured sections for insights, risk signals, supported opportunities, hypotheses, and next checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires transaction hashes or transaction lists; should cite transaction hashes or block references when available and explicitly state missing data.] <br>

## Skill Version(s): <br>
2.0.0 (source: skill.yml, SKILL.md frontmatter, and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
