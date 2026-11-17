## Description:

Searches Hivemind's curated Web3 marketing knowledge base for practitioner insights, frameworks, playbooks, and case studies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[divine-comedian](https://clawhub.ai/user/divine-comedian)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve practitioner-backed Web3 marketing intelligence for strategy, go-to-market research, launch tactics, content creation, and marketing audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials and user queries may be sent to the wrong destination if the configured Hivemind endpoint is untrusted or misconfigured.

Mitigation: Use only a trusted HTTPS Hivemind endpoint and prefer runtime-injected credentials.

Risk: Search queries may contain confidential launch plans, strategy details, or secrets.

Mitigation: Avoid placing confidential information or secrets in search queries.

Risk: The skill does not provide evidence of endpoint allowlisting or destination binding.

Mitigation: Publisher should add endpoint allowlisting or destination binding before broader deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/divine-comedian/skills/myosin-hivemind)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Human-readable CLI text by default, or JSON when raw output is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HIVEMIND_API_URL, HIVEMIND_API_KEY, and HIVEMIND_VERCEL_BYPASS; default maximum is 10 results and documented rate limit is 30 requests per minute.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
