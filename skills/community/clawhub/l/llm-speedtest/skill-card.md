## Description:

Ping major LLM providers in parallel and compare real API latency. Run with /ping

This skill is ready for commercial/non-commercial use.

## Publisher:

[chapati23](https://clawhub.ai/user/chapati23)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to compare live latency across configured LLM providers and check whether a provider appears slow or unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically reads stored provider API keys and sends shell network requests to LLM provider APIs.

Mitigation: Review before installation, run only when live provider calls and small API quota usage are intended, and prefer explicit runtime confirmation with safer secret handling for production or high-value keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chapati23/skills/llm-speedtest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-formatted latency results sorted fastest to slowest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs live API calls with a minimal prompt and reports round-trip latency with status badges.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
