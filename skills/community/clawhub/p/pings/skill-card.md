## Description:

Fetches recent Wink Pings news and, when the user provides or has configured an email, uses it as the user_id to retrieve personalized subscription news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ully](https://clawhub.ai/user/ully)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve current AI or Wink Pings news, optionally personalized through a user-provided email identifier.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic AI-news requests may be routed to Wink Pings rather than another news source.

Mitigation: Review the trigger behavior before installing and enable the skill only when Wink Pings should handle those requests.

Risk: The skill can collect, reuse, or locally store an email address as a user_id for personalized news.

Mitigation: Provide an email only with user consent, avoid logging the full address, and do not store it locally unless the user explicitly approves persistent reuse.

Risk: Email addresses can appear in URL query strings or unpinned npx command examples.

Mitigation: Prefer URL-encoded requests that avoid exposing real addresses in shared logs, and review command provenance before running npx examples.

## Reference(s):

- [Pings skill page](https://clawhub.ai/ully/skills/pings)
- [Wink Pings latest news API](https://wink.run/api/pings/latest)
- [Wink Pings service](https://wink.run)
- [reference.md](artifact/reference.md)
- [examples.md](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown news summaries with URLs, plus optional curl or CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a locally stored email identifier for personalized Wink Pings results when the user consents.]

## Skill Version(s):

1.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
