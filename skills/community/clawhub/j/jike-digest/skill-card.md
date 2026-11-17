## Description:

Fetches the latest posts from a specified Jike Topic, filters recent valuable content, and produces a Simplified Chinese daily Markdown digest with summaries, practical suggestions, and inspiration notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redisread](https://clawhub.ai/user/redisread)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate a daily digest for a chosen Jike Topic, filtering recent posts and turning selected content into concise Markdown analysis. It is useful for monitoring community topics and extracting trends, recommendations, and follow-up ideas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can clean existing output for the current topic and date before writing a new digest.

Mitigation: Set JIKE_DIGEST_BASE_DIR to a dedicated digest directory and review the cleanup behavior before running it against directories that contain files you want to keep.

Risk: The skill depends on a separate autocli Jike command to fetch topic content.

Mitigation: Install and review the autocli Jike command separately, and only run it in environments where that dependency is trusted.

## Reference(s):

- [Output Template](references/output-template.md)
- [ClawHub Skill Page](https://clawhub.ai/redisread/skills/jike-digest)
- [Publisher Profile](https://clawhub.ai/user/redisread)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Simplified Chinese Markdown daily digest with frontmatter, post summaries, value notes, practical suggestions, inspiration notes, topic summary, and top-three selections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches up to 50 posts for one configured topic and filters posts to a recent time window, defaulting to 24 hours.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
