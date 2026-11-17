## Description:

Call GET /api/bilibili/share-url-transfer/v1 for Bilibili Share Link Resolution through JustOneAPI with shareUrl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to resolve shortened Bilibili share URLs into standard video and page identifiers through the JustOneAPI endpoint. It is useful when automating extraction or lookup workflows from Bilibili mobile share links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is passed on the command line and may be exposed through shell history, logs, or process monitoring.

Mitigation: Use a narrowly scoped or disposable token where available, avoid pasting token values into shared outputs, and rotate the token if exposure is suspected.

Risk: The token and Bilibili share URL are sent to JustOneAPI as URL query parameters.

Mitigation: Install only if the user trusts JustOneAPI with those values, and avoid using sensitive share URLs unless that data sharing is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-bilibili-share-url-transfer)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_share_url_transfer&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_share_url_transfer&utm_content=project_link)
- [justoneapi Publisher Profile](https://clawhub.ai/user/justoneapi)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a Bilibili shareUrl query parameter.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
