## Description:

Personalized news briefings that learn your interests, formats, and timing preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to receive personalized news briefings that reflect their interests, preferred format, timing, and engagement history. Agents use it to build a local news profile, cite sources by name, and handle contested topics with multi-source coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores news preferences and engagement history locally under ~/news/.

Mitigation: Review or delete the local ~/news/ files if ongoing personalization is not desired.

Risk: News briefings can become stale or misleading if current events are not verified.

Mitigation: Check source freshness, include when news broke, cite sources by name, and use multiple sources for contested topics.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/news)
- [Publisher Profile](https://clawhub.ai/user/ivangdavila)
- [Skill Homepage](https://clawic.com/skills/news)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration]

**Output Format:** [Markdown briefings and preference prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain local preference and engagement files under ~/news/.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
