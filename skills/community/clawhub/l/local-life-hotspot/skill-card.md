## Description:

Searches for current hot topics, selects one topic for deeper Xiaohongshu-oriented copy, generates a simple title image, and can publish automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[githubsoftware2015](https://clawhub.ai/user/githubsoftware2015)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and social media operators use this skill to find a current topic in a chosen domain, draft structured Xiaohongshu content, generate a simple cover image, and optionally publish through a Xiaohongshu MCP integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish to a linked Xiaohongshu account automatically.

Mitigation: Keep auto-publish disabled until the draft is reviewed and a final confirmation step is added.

Risk: Topic queries are sent to Jina services and page content may be fetched through Jina Reader.

Mitigation: Use only non-sensitive topics and keywords that are acceptable to send to third-party services.

Risk: Security evidence reports disabled TLS verification and an unsafe shell=True publishing path.

Mitigation: Restore certificate verification and replace shell command construction with argument-safe publishing before trusted deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/githubsoftware2015/skills/local-life-hotspot)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands]

**Output Format:** [Markdown draft plus console status text and an optional JPEG image file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write a draft file and publish to Xiaohongshu when auto-publish is enabled.]

## Skill Version(s):

6.0.0 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
