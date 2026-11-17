## Description:

Deconstruct video ad creatives into marketing dimensions using Gemini AI, including hooks, social proof, CTAs, target audience, emotional triggers, urgency tactics, and related marketing patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fortytwode](https://clawhub.ai/user/fortytwode)

### License/Terms of Use:


## Use Case:

Marketing teams, creative strategists, and developers use this skill to analyze video ad creatives, understand persuasive patterns, and generate structured briefs or downstream JSON analysis for consumer product and gaming ads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video ad inputs may contain confidential or unreleased creative material that is sent to Gemini or Vertex AI for analysis.

Mitigation: Use the skill only under approved Gemini or Vertex AI data handling terms, avoid confidential inputs unless permitted, and run with a least-privileged Google service account.

Risk: Generated marketing analysis may be inaccurate or influenced by prompt-injection text embedded in competitor ads.

Mitigation: Treat generated summaries and JSON as untrusted analysis output and review findings before using them in briefs, decisions, or downstream automation.

Risk: Runtime behavior depends on external model availability, credentials, and rate limits.

Mitigation: Install in an isolated Python environment with pinned dependencies, configure credentials explicitly, and account for retries or rate-limit failures in calling workflows.

## Reference(s):

- [Meta Video Ad Deconstructor on ClawHub](https://clawhub.ai/fortytwode/skills/meta-video-ad-deconstructor)
- [Publisher profile: fortytwode](https://clawhub.ai/user/fortytwode)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Plain text summaries, markdown guidance, Python code examples, and structured JSON analysis objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces summary text and per-dimension marketing analysis keyed by dimension name; progress callbacks may report analysis status.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
