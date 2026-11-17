## Description:

Search Xiaohongshu notes, inspect creator profiles, resolve share links, and drill into note comments, replies, and note detail endpoints through JustOneAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to retrieve structured Xiaohongshu note, creator, comment, reply, and share-link data through JustOneAPI when given keywords, note IDs, user IDs, share URLs, or pagination cursors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command arguments, URLs, or process logging.

Mitigation: Use a narrowly scoped, revocable token where available, avoid environments that log process arguments or full request URLs, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should summarize the concrete Xiaohongshu result first and include backend payloads when an API call fails.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
