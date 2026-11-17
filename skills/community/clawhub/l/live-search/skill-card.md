## Description:

Live Search helps an agent fetch fresh public web results through a host-provided local search gateway when the user needs current information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codenova58](https://clawhub.ai/user/codenova58)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when an answer depends on current public web data, including news, prices, weather, scores, rates, fact checks, or other information after the model knowledge cutoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may reveal sensitive intent or private information to the host search gateway.

Mitigation: Do not include secrets, credentials, private documents, or sensitive personal details in search terms.

Risk: Returned links and snippets come from the public web and may be incorrect, stale, or unsafe.

Mitigation: Treat links as untrusted and verify important facts at their original sources before relying on them.

## Reference(s):

- [ClawHub skill page: Live Search](https://clawhub.ai/codenova58/skills/live-search)
- [ClawHub publisher profile: codenova58](https://clawhub.ai/user/codenova58)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown result lists with optional concise analysis and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary search results are expected to preserve the gateway-provided message block before any added analysis.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
