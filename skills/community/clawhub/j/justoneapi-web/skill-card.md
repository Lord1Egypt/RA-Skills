## Description:

Analyze Web Page workflows with JustOneAPI, including HTML content, rendered HTML content, and markdown content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch a web page as raw HTML, rendered HTML, or markdown through JustOneAPI when they need API-backed page content for analysis or workflow automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command-line or query-string handling.

Mitigation: Use a narrowly scoped token, keep it out of chat and logs, rotate it regularly, and avoid running the helper where process arguments are visible to untrusted users.

Risk: Requested URLs may be visible in local process metadata or API-side logs.

Mitigation: Avoid submitting sensitive, internal, private, or credential-bearing URLs through this skill.

Risk: The skill fetches user-supplied web content, which can return untrusted HTML or markdown.

Mitigation: Treat returned page content as untrusted data and review it before using it in downstream actions or generated outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-web)
- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_web&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN. Operations require a user-supplied url parameter.]

## Skill Version(s):

1.0.6 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
