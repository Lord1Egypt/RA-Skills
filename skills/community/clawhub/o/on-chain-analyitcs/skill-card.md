## Description:

Analyzes EVM smart contracts by fetching or accepting ABIs, discovering usage patterns, generating Dune-based analytics, and returning structured results for supported chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramitphi](https://clawhub.ai/user/ramitphi)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to inspect verified EVM contracts, understand function usage, identify top callers, and generate dashboard-ready on-chain activity summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contract addresses, chain names, and manually supplied ABI JSON are sent to an external on-chain analysis service.

Mitigation: Submit only public or approved contract data, and avoid proprietary or sensitive ABI data unless external processing is acceptable.

Risk: Dune queries or dashboard links may be created and retained for later viewing.

Mitigation: Review generated query and dashboard links before sharing them, especially when a manual ABI was supplied.

Risk: Generated analytics may be incomplete, empty, delayed, or affected by external service availability.

Mitigation: Treat results as analytical assistance and verify important findings against source transactions or Dune query output before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ramitphi/skills/on-chain-analyitcs)
- [On-chain analysis API endpoint](https://esraarlhpxraucslsdle.supabase.co/functions/v1/onchain-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, json, api calls, guidance]

**Output Format:** [Markdown summaries with structured JSON results, dashboard links, and Dune query links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis may take 2-5 minutes and can include empty or failed query results when source contract activity or external services are limited.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
