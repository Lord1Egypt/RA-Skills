## Description:

Search, summarize, and extract insights from your Limitless AI pendant life logs, including keyword and semantic search, date range queries, memory recall, and action item extraction for named agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremytoce](https://clawhub.ai/user/jeremytoce)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search and summarize Limitless lifelog transcripts, recall prior conversations, and extract action items associated with configured agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses private Limitless lifelog transcripts.

Mitigation: Install and use it only when the user is comfortable granting transcript access through LIMITLESS_API_KEY, and limit shared excerpts to what is needed for the request.

Risk: Action item dispatch can send transcript excerpts to configurable webhook or email destinations.

Mitigation: Use dispatch only after confirming the roster path, verifying each destination, and previewing or minimizing outbound payloads.

Risk: Server security evidence marked the release as suspicious due to incomplete safeguards around private transcript dispatch.

Mitigation: Review the skill carefully before installation and keep dispatch disabled until recipient URLs or email addresses are explicitly confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeremytoce/skills/limitless-lifelogs)
- [Publisher profile](https://clawhub.ai/user/jeremytoce)
- [Limitless API base URL](https://api.limitless.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and structured text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include timestamps, excerpts, log IDs, action item summaries, and user-confirmed dispatch payload guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
