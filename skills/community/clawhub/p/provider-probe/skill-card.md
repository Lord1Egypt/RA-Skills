## Description:

Probe and verify whether an OpenAI-compatible baseURL is a real single-model endpoint or a multi-model aggregation pool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit OpenAI-compatible model providers, inspect endpoint behavior, and decide whether a provider should be used as a primary route, fallback route, or avoided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed when passed directly on the command line or used with untrusted provider URLs.

Mitigation: Use least-privilege test keys, avoid production credentials, and prefer secret handling that does not expose keys through shell history or process listings.

Risk: Provider URLs may send prompts, metadata, and probe results to services that are not trusted or sufficiently validated.

Mitigation: Probe only trusted HTTPS endpoints and treat all submitted test prompts and metadata as visible to the provider.

Risk: Public API behavior cannot prove official upstream model provenance with certainty.

Mitigation: Present findings as confidence-based operational judgments and avoid claiming definitive vendor provenance from probe behavior alone.

## Reference(s):

- [Provider Probe Checklist](references/provider-probe-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/andyrenxu7255/skills/provider-probe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with optional JSON probe output and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports tested config facts, model catalog findings, endpoint compatibility, stability runs, capability checks, trust judgment, and primary/fallback/avoid recommendation.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
