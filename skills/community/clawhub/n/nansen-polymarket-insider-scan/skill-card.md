## Description: <br>
Scan a resolved Polymarket market for wallets exhibiting suspicious trading patterns: fresh funding, single-market focus, extreme ROI, late entry at high prices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and investigators use this skill to scan resolved Polymarket markets with Nansen CLI data and identify wallets whose trading patterns merit further review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Nansen API key and nansen CLI access. <br>
Mitigation: Use an appropriately scoped NANSEN_API_KEY, manage it as a secret, and run the CLI only in trusted environments. <br>
Risk: The security guidance notes trust in an unpinned nansen-cli package. <br>
Mitigation: Pin and review the CLI package version in controlled deployments before execution. <br>
Risk: Wallet scores are investigative heuristics and may be mistaken for proof of wrongdoing. <br>
Mitigation: Use the scores as leads for human review and corroborate findings before taking action. <br>
Risk: Rate limits or per-wallet errors can leave some wallet activity unreviewed. <br>
Mitigation: Use pacing, pagination, and follow-up review for skipped or errored wallets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-polymarket-insider-scan) <br>
- [Publisher profile](https://clawhub.ai/user/nansen-devops) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and scoring guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NANSEN_API_KEY and the nansen CLI; wallet scores are investigative heuristics.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
