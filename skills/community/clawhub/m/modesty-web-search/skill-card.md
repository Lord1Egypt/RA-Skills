## Description:

Searches the web through SkillBoss API Hub for current information, news, images, and videos with filters for result type, time range, region, and safe search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run web, news, image, and video searches when a task requires current online information or source discovery. It can return immediate results or save formatted search output for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to the disclosed SkillBoss/HeyBoss API and may expose sensitive terms if users include confidential information.

Mitigation: Do not include secrets, credentials, private customer data, or confidential internal project names in search queries.

Risk: Using file output can leave search results on disk.

Mitigation: Use the output file option only when the saved results are intended to persist and can be stored in the selected location.

Risk: The skill depends on trust in the external SkillBoss/HeyBoss service and an API key.

Mitigation: Confirm the service and API key handling are acceptable before installation or use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/modesty-web-search)
- [SkillBoss setup guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text, Markdown, or JSON search results, with optional file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends user-provided search queries to the SkillBoss/HeyBoss API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
