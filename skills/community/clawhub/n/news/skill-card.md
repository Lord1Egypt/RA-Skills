## Description: <br>
Personalized news briefings that learn your interests, formats, and timing preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to build a local news profile, deliver personalized briefings, and adapt coverage based on stated interests and engagement history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local preference and engagement files may preserve sensitive interests or reading patterns. <br>
Mitigation: Review or edit ~/news/memory.md, ~/news/history.md, and ~/news/sources.md when interests change or should not be reused. <br>
Risk: News briefings can be misleading if stale, uncertain, or unsupported events are presented as current facts. <br>
Mitigation: Lead with what happened, include when news broke, cite sources by name, and state uncertainty instead of fabricating events. <br>
Risk: Contested topics can be distorted by single-source coverage. <br>
Mitigation: Use at least two sources, note disagreements, and identify editorial leanings when relevant. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/news) <br>
- [Project homepage](https://clawic.com/skills/news) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown news briefings with source names, timestamps, and local preference notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local profile, source, and engagement history files under ~/news/ when present.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
