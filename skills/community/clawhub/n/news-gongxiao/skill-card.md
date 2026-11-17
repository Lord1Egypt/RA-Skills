## Description:

Retrieves Chinese-language daily news summaries and article details through a disclosed API, with support for date queries, hot rankings, category filtering, and detail reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vic240821](https://clawhub.ai/user/vic240821)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve daily news summaries, hot news rankings, date-specific news lists, category-filtered news, and article details in Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts api.cjiot.cc when invoked, so prompts that loosely mention news could trigger third-party API requests.

Mitigation: Narrow activation phrases or confirm with the user before API calls when intent is ambiguous.

Risk: The tool is Chinese-language and depends on a disclosed third-party news API.

Mitigation: Install only in environments where that language scope and external API dependency are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vic240821/skills/news-gongxiao)
- [API homepage](https://api.cjiot.cc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown news summaries and article details with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API-derived article metadata such as title, summary, heat score, category, and publish time.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
