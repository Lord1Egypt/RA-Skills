## Description: <br>
Negotiate on behalf of your principal with hard limits, graduated autonomy, and mandatory human approval for commitments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to draft, evaluate, and conduct bounded negotiations for buying, selling, peer-to-peer marketplaces, and professional agreements while preserving explicit principal approval for commitments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent could accept, counteroffer, or disclose sensitive leverage without the principal's informed approval. <br>
Mitigation: Keep autonomy at Level 1 unless the principal grants a higher level for the specific category, require approval for commitments, and define hard limits, targets, walk-away rules, and approval thresholds before use. <br>
Risk: Salary, contract, large purchase, or sensitive marketplace negotiations may expose personal leverage details or create high-impact obligations. <br>
Mitigation: Use low autonomy for sensitive negotiations, log offers and decisions, and store only negotiation history or personal leverage details the principal is comfortable reusing later. <br>
Risk: Unusual payment terms, off-platform requests, pressure tactics, or conditions near the hard limit can increase fraud, coercion, or miscommitment risk. <br>
Mitigation: Escalate to the principal when terms are unusual, payment moves off-platform, pressure tactics appear, or a deal approaches the hard limit or approval threshold. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ivangdavila/negotiate) <br>
- [Buying negotiations](buying.md) <br>
- [Selling negotiations](selling.md) <br>
- [P2P marketplace negotiations](p2p.md) <br>
- [Professional negotiations](professional.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with structured negotiation parameters, escalation triggers, and message drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code, API calls, or tool invocations are produced by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
