## Description:

Generates a Chinese daily digest of the top Hacker News articles with summaries, key points, practical takeaways, inspiration, and social posts for Jike, Xiaohongshu, and Twitter/X.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redisread](https://clawhub.ai/user/redisread)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect the current Hacker News Top 10, fetch article content, and produce a Chinese markdown daily digest with article analysis and social media copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overwrite the dated digest file and clear temporary files under the dated output path.

Mitigation: Configure BASE_DIR to a dedicated folder before running the skill.

Risk: The browser fallback broadens web access during article retrieval.

Mitigation: Use the fallback only for the intended Hacker News article workflow and avoid sensitive or unrelated sites.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redisread/skills/hackernews-digest)
- [Publisher profile](https://clawhub.ai/user/redisread)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown daily digest with article sections and social media copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a dated digest file and temporary per-article markdown files under the configured base directory.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
