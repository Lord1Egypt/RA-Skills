## Description:

Call GET /api/v1/google/lens for Google SERP Lens through Just Serp API with url.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Just Serp API's Google Lens endpoint for visual search analysis, product matching, visual matches, exact duplicate checks, and related links from a public image URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public image URLs and query options are sent to Just Serp API for Google Lens processing.

Mitigation: Use only public, non-sensitive image URLs and review query options before execution.

Risk: The documented helper passes JUST_SERP_API_KEY as a command-line argument, which may be exposed through process listings or logs.

Mitigation: Prefer reading the key directly from the environment where possible, avoid logging commands containing secrets, and rotate the key if it may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justserpapi/skills/justserpapi-google-lens)
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_lens&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_lens&utm_content=project_link)
- [Generated operation reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JUST_SERP_API_KEY value and a publicly accessible image URL.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
