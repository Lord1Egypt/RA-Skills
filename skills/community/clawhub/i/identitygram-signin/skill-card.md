## Description:

Sign in to IdentityGram by calling the /auth/signin endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waqas-orcalo](https://clawhub.ai/user/waqas-orcalo)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to authenticate a user with IdentityGram credentials through OpenClaw's skill system and receive the sign-in response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles IdentityGram email and password values directly as normal skill inputs.

Mitigation: Install and invoke it only when the publisher is trusted and the agent is intended to handle those credentials.

Risk: The skill can return full authentication tokens and raw sign-in responses.

Mitigation: Treat token, accessToken, refreshToken, raw, and user fields as secrets; avoid displaying, logging, storing, or passing them to other skills unless strictly necessary.

Risk: The skill depends on the configured IdentityGram HTTPS authentication endpoint being the intended service.

Mitigation: Confirm the endpoint and service availability before use, and stop using the skill if the endpoint cannot be verified.

## Reference(s):

- [Identitygram Signin on ClawHub](https://clawhub.ai/waqas-orcalo/skills/identitygram-signin)
- [IdentityGram sign-in endpoint](https://gateway-v2.identitygram.co.uk/auth/signin)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON response fields with supporting Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include raw IdentityGram responses, success status, token fields, user information, and status messages; returned token fields should be treated as secrets.]

## Skill Version(s):

0.0.2 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
