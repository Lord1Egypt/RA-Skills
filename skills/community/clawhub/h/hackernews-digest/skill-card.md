## Description: <br>
Generates a Chinese daily digest of the top 10 Hacker News stories with summaries, key takeaways, practical advice, inspiration, and social copy for Jike, Xiaohongshu, and Twitter/X. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redisread](https://clawhub.ai/user/redisread) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technology readers use this skill to fetch current Hacker News stories and produce a structured Chinese daily digest for review, learning, and social sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reruns can overwrite or remove same-day generated digest output and temporary files in the configured base directory. <br>
Mitigation: Set --base-dir or HN_DIGEST_BASE_DIR to a dedicated Hacker News digest folder that does not contain unrelated work. <br>
Risk: The skill fetches public article URLs and may produce summaries or social copy from inaccessible or incomplete source content. <br>
Mitigation: Review the generated digest before relying on it or publishing the social media copy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redisread/hackernews-digest) <br>
- [Publisher profile](https://clawhub.ai/user/redisread) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration] <br>
**Output Format:** [Markdown daily digest with YAML front matter and article-level sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes same-day temporary article files and a final hackernews-daily-{YYYYMMDD}.md file under the configured base directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
