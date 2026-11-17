## Description:

Call GET /api/kuaishou/share-url-transfer/v1 for Kuaishou Share Link Resolution through JustOneAPI with shareUrl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to resolve Kuaishou share URLs through JustOneAPI and retrieve the resolved content identifier and target object data for automated content processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token can be exposed through process arguments or URL logs.

Mitigation: Use a limited-scope or quota-limited JustOneAPI token, avoid shared systems where process arguments may be visible, and rotate the token if logs may have captured it.

Risk: The skill sends the Kuaishou share URL and JustOneAPI token to a third-party API service.

Mitigation: Install and run the skill only when the user trusts JustOneAPI with the submitted share URL and token.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-kuaishou-share-url-transfer)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_share_url_transfer&utm_content=project_link)
- [Kuaishou Share Link Resolution Operations](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes the operation and endpoint before returning the backend JSON response; backend errors include the payload and operation ID.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
