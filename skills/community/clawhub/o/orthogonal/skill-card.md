## Description:

Orthogonal API Platform helps agents search, discover, integrate, and call paid APIs using the Orthogonal SDK, Run API, or x402 direct payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christianpickettcode](https://clawhub.ai/user/christianpickettcode)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to discover paid APIs, inspect endpoint requirements, generate integration snippets, and make API calls through Orthogonal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may make paid API calls or direct x402 payments without sufficient user control.

Mitigation: Require explicit approval for each paid call and set spending limits where possible.

Risk: Prompts, internal URLs, API keys, or wallet private keys may be exposed to external services.

Mitigation: Avoid sending confidential prompts or internal URLs, keep credentials narrowly scoped, and protect wallet private keys.

Risk: Installing or using the SDK may add unreviewed dependency risk.

Mitigation: Pin and review the SDK before installation.

## Reference(s):

- [Orthogonal](https://orthogonal.com)
- [Orthogonal Documentation](https://orthogonal.com/dashboard/docs)
- [Browse Orthogonal APIs](https://orthogonal.com/discover)
- [ClawHub Skill Page](https://clawhub.ai/christianpickettcode/skills/orthogonal)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline JSON, JavaScript, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to make paid API calls or direct x402 payments; each paid call should require explicit user approval.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
