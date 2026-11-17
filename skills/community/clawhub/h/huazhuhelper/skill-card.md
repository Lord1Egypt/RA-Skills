## Description:

huazhuhelper helps agents query Huazhu hotel lists through Huazhu OpenAPI using OAuth2 credentials supplied by the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjinliang1991](https://clawhub.ai/user/wangjinliang1991)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate guidance and Python examples for authenticating to Huazhu OpenAPI and retrieving hotel-list data. It is intended for Huazhu hotel-list queries where the user can provide valid client credentials and distributor configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill workflow requires Huazhu clientId and clientSecret values and includes examples that place credentials directly in code.

Mitigation: Use a secret manager or environment variables, and do not paste production clientSecret values into chat transcripts or source files.

Risk: The example prints part of the bearer token after OAuth authentication.

Mitigation: Remove token printing and redact authentication material from logs before using the generated code.

Risk: The test hotel-list endpoint shown in the artifact uses HTTP.

Mitigation: Change the hotel API endpoint to HTTPS or confirm an equivalent secure endpoint before transmitting credentials or bearer tokens.

Risk: The OAuth example requests the broad ALL scope.

Mitigation: Reduce OAuth scope if Huazhu supports narrower permissions for hotel-list queries.

Risk: Credentials may be sent for tasks outside the intended Huazhu hotel-list workflow.

Mitigation: Confirm the user is specifically requesting Huazhu hotel-list data before collecting credentials or sending API requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjinliang1991/skills/huazhuhelper)
- [ClawHub publisher profile](https://clawhub.ai/user/wangjinliang1991)
- [Huazhu test OAuth endpoint](https://test-oauth2-api.huazhu.com)
- [Huazhu production OpenAPI endpoint](https://openapi.huazhu.com)
- [Huazhu test hotel endpoint](http://test-crs-distributor.huazhu.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OAuth credential handling guidance, API endpoint configuration, and hotel-list query examples.]

## Skill Version(s):

1.0.3 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
