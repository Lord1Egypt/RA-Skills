## Description:

Search and extract Google data through the KeyAPI REST API using live official docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyzzero](https://clawhub.ai/user/xyzzero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent operators use this skill to perform Google web, vertical, local, visual, and webpage research through KeyAPI, with docs-verified endpoint selection and credential-aware execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential setup can store a KeyAPI token in shell profile files in plaintext.

Mitigation: Prefer setting KEYAPI_TOKEN only for the current session or using a dedicated secret store; avoid passing real tokens with --token and rotate any token that may have been exposed in terminal history or a shell profile.

## Reference(s):

- [KeyAPI documentation index](https://docs.keyapi.ai/llms.txt)
- [KeyAPI Google documentation](https://docs.keyapi.ai/en/google/)
- [Google search docs](https://docs.keyapi.ai/en/google/search.md)
- [Google webpage extraction docs](https://docs.keyapi.ai/en/google/webpage.md)
- [Google images docs](https://docs.keyapi.ai/en/google/images.md)
- [Google Lens docs](https://docs.keyapi.ai/en/google/lens.md)
- [Google places docs](https://docs.keyapi.ai/en/google/places.md)
- [Google reviews docs](https://docs.keyapi.ai/en/google/reviews.md)
- [Scenario Cards](references/scenarios.md)
- [Routing Policy](references/routing-policy.md)
- [Setup And Auth](references/setup-and-auth.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, JSON API previews or results, and saved JSON files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a KeyAPI bearer token for live requests; helper scripts can preview large responses or save complete JSON to an output file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
