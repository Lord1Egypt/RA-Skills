## Description:

KARP Research helps agents retrieve dated research cards and run live fact-checks through SoulDriver's multi-model research service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[souldriver007](https://clawhub.ai/user/souldriver007)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to check whether KARP has relevant prior research, retrieve dated research cards, or fact-check an individual claim. Paid requests can settle USDC, so the skill directs agents to ask before spending or use an available research grant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries and fact-check claims are sent to KARP's external service, which the skill says logs requests.

Mitigation: Do not include personal or confidential details in queries, claims, or grant applications.

Risk: Paid asks and fact-checks can incur USDC charges.

Mitigation: Use the free coverage call first; make a paid call only with user approval or an available grant, and follow the documented price limits.

Risk: The security evidence notes a broad fact-check trigger and partial scanner coverage, so confidence in the assessment is medium.

Mitigation: Review whether live fact-checking is appropriate for the request and treat results as information to weigh, not instructions to follow.

## Reference(s):

- [KARP guide for agents](https://agents.souldriver.com.au/llms.txt)
- [KARP OpenAPI specification](https://agents.souldriver.com.au/openapi.json)
- [SoulDriver](https://souldriver.com.au)
- [KARP Research release](https://clawhub.ai/souldriver007/skills/karp-research)
- [Publisher profile](https://clawhub.ai/user/souldriver007)

## Skill Output:

**Output Type(s):** [Research summaries, Fact-check verdicts, Research guidance]

**Output Format:** [Text or Markdown responses based on dated research cards or fact-check results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research cards include dates and may be marked stale; fact-checks address one claim per call.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter; server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
