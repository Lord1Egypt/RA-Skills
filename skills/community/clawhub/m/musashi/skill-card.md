## Description:

Conviction-weighted token intelligence. Analyze any token through 7 elimination gates, cross-domain pattern detection, and adversarial debate. Triggers on "analyze token", "musashi scan", "check conviction", "narrative meta".

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeheskieltame](https://clawhub.ai/user/yeheskieltame)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Musashi to evaluate crypto tokens through gated safety, liquidity, wallet, social, narrative, market timing, and cross-validation checks. The skill can produce analysis-only verdicts without a private key, and can optionally publish high-conviction STRIKE records on-chain after explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish on-chain records and run admin-style blockchain write commands when publish mode is configured.

Mitigation: Use analysis mode without a private key when possible, and review every transaction prompt before approving any on-chain action.

Risk: Private-key handling is security-sensitive and was flagged by the server security evidence.

Mitigation: Use a dedicated low-balance wallet for Musashi operations and avoid using a main wallet or broadly funded key.

Risk: Crypto-token analysis can be misleading or financially harmful if outputs are treated as investment advice.

Mitigation: Require explicit token confirmation before analysis and treat PASS/FAIL results as decision-support signals that need human review.

## Reference(s):

- [Musashi Skill Page](https://clawhub.ai/yeheskieltame/skills/musashi)
- [Gate Reference](references/GATES.md)
- [Pattern Detection Reference](references/PATTERNS.md)
- [API Endpoints Reference](references/API_ENDPOINTS.md)
- [0G Storage CLI Install Docs](https://docs.0g.ai/developer-hub/building-on-0g/storage/storage-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PASS/FAIL gate results, specialist analyses, debate summaries, conviction judgments, configuration snippets, transaction prompts, transaction hashes, explorer links, and storage hashes.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
