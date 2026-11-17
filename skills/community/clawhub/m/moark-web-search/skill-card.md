## Description:

Search web content such as webpages, images, and videos using the /web-search API with an Access Token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fchange](https://clawhub.ai/user/fchange)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run web, image, or video searches through the Gitee AI web-search API and summarize the returned JSON results for a user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to the Gitee AI web-search service.

Mitigation: Install and use the skill only when that service is trusted and sending the intended queries to it is acceptable.

Risk: Passing the API key on the command line can expose credentials through shell history or process listings.

Mitigation: Prefer setting GITEEAI_API_KEY in a protected environment instead of using --api-key.

Risk: Runtime dependencies may change if installed without pinning.

Mitigation: Install dependencies in a virtual environment with pinned versions when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fchange/skills/moark-web-search)
- [Gitee AI web-search endpoint](https://ai.gitee.com/v1/web-search)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GITEEAI_API_KEY access token; search result count is limited to 1-50 by the bundled script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
