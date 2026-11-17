## Description:

Research answers and live fact-checks from KARP, SoulDriver's multi-model research engine (GPT, Gemini, Grok and Claude). Check free whether KARP has researched a question, get dated research cards ($0.03), or fact-check one claim with four web-searching models ($0.25). Pay per call with x402 (USDC on Base or Solana), or start with a free research grant if you have no wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[souldriver007](https://clawhub.ai/user/souldriver007)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use KARP to check whether a question has relevant research, retrieve dated multi-model research cards, or request a live check of an individual claim. Paid asks and checks require the user's authorization or an available research grant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research questions and claims are sent to an external service, and the skill documentation says KARP logs requests.

Mitigation: Do not include personal or confidential details in questions or claims; consider whether external processing is appropriate for the task.

Risk: The security review is incomplete because a referenced local path was missing during scanning.

Mitigation: Resolve the missing path and review it before treating the scan as complete.

## Reference(s):

- [Guide for agents](https://agents.souldriver.com.au/llms.txt)
- [KARP OpenAPI specification](https://agents.souldriver.com.au/openapi.json)
- [SoulDriver](https://souldriver.com.au)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Research summaries, dated research cards, and fact-check results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research cards include dates and may be marked stale; fact-check results include a verdict, confidence, reasoning, and sources.]

## Skill Version(s):

1.0.0 (source: frontmatter; server release metadata confirms 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
