## Description: <br>
Sign in to IdentityGram by calling the /auth/signin endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waqas-orcalo](https://clawhub.ai/user/waqas-orcalo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to authenticate a user with IdentityGram credentials and receive the sign-in response for downstream account workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends an IdentityGram email and password to an external sign-in endpoint. <br>
Mitigation: Use only with trusted IdentityGram credentials and confirm the endpoint is intended for the target environment before invoking the skill. <br>
Risk: The response may include access or refresh tokens that can grant account access. <br>
Mitigation: Treat returned tokens like passwords and keep them out of chats, logs, screenshots, and unrelated tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/waqas-orcalo/identitygram-signin) <br>
- [IdentityGram sign-in endpoint](https://gateway-v2.identitygram.co.uk/auth/signin) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authentication status, user information, access tokens, and refresh tokens from IdentityGram.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
