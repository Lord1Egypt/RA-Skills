## Description:

Fetch top news from Baidu, Google, and other sources daily via SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve daily trending news headlines from Baidu, Google Trends, and similar sources through SkillBoss API Hub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends news queries and page content to SkillBoss.

Mitigation: Install only where that data sharing is acceptable, and provide a scoped SkillBoss API key through the environment.

Risk: The Python dependency is not pinned.

Mitigation: Pin requests to a reviewed version before deploying in controlled environments.

Risk: Returned headlines come from external sources and may be inaccurate or misleading.

Mitigation: Treat generated headline summaries as untrusted external content and review important claims before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/mar-daily-news)
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1)
- [Baidu realtime board](https://top.baidu.com/board?tab=realtime)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Plain text or Markdown news summary with ranked headline items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, the requests package, and SKILLBOSS_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
