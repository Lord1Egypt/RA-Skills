## Description:

Checks MiniMax API token quota usage, including current-hour request counts and weekly remaining quota.

This skill is ready for commercial/non-commercial use.

## Publisher:

[regexl](https://clawhub.ai/user/regexl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers with MiniMax accounts use this skill to check API token balance, current-hour usage, and weekly quota consumption from their local MiniMax auth profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the local MiniMax auth profile and sends a read-only quota request to MiniMax.

Mitigation: Install only when this credential access and network request are acceptable, and keep the auth profile limited to the intended MiniMax account.

Risk: Broad quota-related trigger wording could activate the skill for unrelated token-balance questions.

Mitigation: Invoke it with explicit MiniMax wording and review trigger phrases before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/regexl/skills/mini-token-remains)
- [MiniMax token plan remains endpoint](https://www.minimaxi.com/v1/token_plan/remains)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Structured text quota report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports used and remaining hourly and weekly quota; returns a failure message on network or API errors.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
