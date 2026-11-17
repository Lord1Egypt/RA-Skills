## Description:

Query usage statistics and quota from a user-specified new-api endpoint. Use when the user asks to check API quota, usage records, token consumption, model-level usage, or remaining balance. Requires explicit --base-url and --key input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang48](https://clawhub.ai/user/wang48)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to query quota, usage records, token consumption, model-level usage, and remaining balance for a user-specified new-api deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be exposed because the usage request places the key in the URL, which may be logged by the destination or infrastructure.

Mitigation: Use only a narrowly scoped key with trusted endpoints, and prefer endpoints or wrappers that authenticate only with an Authorization header.

Risk: The user-supplied base URL may point to an untrusted or non-HTTPS destination.

Mitigation: Use only trusted HTTPS new-api endpoints and confirm unknown endpoints before sending credentials.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples; script output is plain text tables or JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit base URL and API key inputs; default usage filtering is local-timezone today only.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
