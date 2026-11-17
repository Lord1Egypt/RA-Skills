## Description:

Bilingual search-layer skill for OpenClaw that turns ordinary web lookup into multi-source retrieval, intent-aware ranking, adaptive weighting, thread-pulling research, Chinese-query optimization, and finance-aware realtime prioritization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wewehg](https://clawhub.ai/user/wewehg)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research-oriented agents use this skill to improve web lookup with broader source coverage, intent-aware ranking, Chinese-query handling, thread-following research, and realtime finance prioritization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad outbound web and API requests may fetch untrusted or unintended URLs.

Mitigation: Constrain allowed providers or domains where possible, review target URLs before deep fetches, and add private-network URL blocking plus redirect validation before deployment.

Risk: The skill may reuse configured provider keys or GitHub credentials automatically.

Mitigation: Use least-privileged environment credentials, avoid broad personal tokens, and require explicit opt-in before reading local GitHub credentials.

Risk: Recursive thread pulling can expand the amount of fetched content and network activity.

Mitigation: Keep depth and per-level limits low, require user approval for recursive crawling, and log followed URLs for review.

Risk: Fetched page or comment content may be sent to external LLM providers for relevance or synthesis.

Mitigation: Do not run the skill on private or sensitive URLs unless the user has approved the provider path; redact sensitive content before LLM processing.

## Reference(s):

- [Intent Classification Guide](references/intent-guide.md)
- [Authority Domain Weights](references/authority-domains.json)
- [research-light Regression Samples](references/research-light-regression-samples.md)
- [ClawHub Skill Page](https://clawhub.ai/wewehg/skills/openclaw-glasses)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with citations and caveats; helper scripts may emit JSON and shell-command workflows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include ranked links, source summaries, provider notes, and conflict callouts depending on available search credentials and selected mode.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
