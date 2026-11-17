## Description:

Scores and ranks skill improvement candidates using heuristic rules, evaluator evidence, LLM-as-judge review, and multi-reviewer blind panels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to evaluate proposed skill improvements, compare candidates, and produce explainable scoring artifacts before execution or gate review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime evaluation of untrusted skill paths can load local Python code in process.

Mitigation: Run runtime evaluation only inside a controlled sandbox and review the target path before execution.

Risk: accept_for_execution recommendations are gate-adjacent and could be mistaken for final approval.

Mitigation: Require a separate execution or release gate before applying any recommended candidate.

Risk: Human-review receipts are advisory unless real signer verification is added.

Mitigation: Treat receipts as supporting evidence and verify reviewers through an independent signing or approval process.

Risk: LLM judge mode can send candidate and target content to external model providers when configured.

Mitigation: Use mock or approved provider configurations for sensitive content, and limit provider credentials to controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanyasheng/skills/improvement-discriminator)
- [ClawHub publisher profile](https://clawhub.ai/user/lanyasheng)

## Skill Output:

**Output Type(s):** [JSON, guidance, shell commands]

**Output Format:** [JSON scoring artifact with ranked candidates, recommendations, blockers, panel reviews, and LLM verdicts when enabled]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit the output artifact path on the command line; LLM judge mode may use external model providers when configured.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
