## Description:

Searches Google through Serper and extracts full-page content from each result with trafilatura for web research, current events, factual lookups, product comparisons, technical documentation, and other up-to-date internet questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nesdeq](https://clawhub.ai/user/nesdeq)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agents use this skill to run Google/Serper searches and receive streamed JSON results enriched with extracted full-page text for research and current information needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic full-page extraction may fetch unvalidated result pages from the user's environment, including internal web services, cloud metadata endpoints, or private networks.

Mitigation: Run the skill in a restricted network sandbox or require URL validation before automatic page extraction.

Risk: Search queries and fetched pages may expose secrets or sensitive internal context to external services.

Mitigation: Avoid entering secrets or sensitive internal queries.

Risk: Runtime dependency installation can introduce supply-chain exposure.

Mitigation: Use a pinned trafilatura dependency in an isolated virtual environment.

## Reference(s):

- [Serper API](https://serper.dev)
- [ClawHub skill page](https://clawhub.ai/nesdeq/skills/openclaw-serper)
- [Agent Skills specification](spec/specification.mdx)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Streamed JSON array with search metadata and extracted page-content results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full-page extraction falls back to snippets when extraction fails; default mode returns five web results and current mode combines recent web and news results.]

## Skill Version(s):

3.1.1 (source: server release and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
