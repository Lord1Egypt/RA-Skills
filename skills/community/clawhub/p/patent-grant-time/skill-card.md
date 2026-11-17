## Description:

Uses recently granted Chinese invention patents in a user's technical field to estimate filing-to-grant timelines, including median, fast, and slow cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Patent applicants, agents, and project planners use the skill to estimate field-specific Chinese invention-patent grant timelines from recent granted patents and plan around filing, reporting, or financing milestones.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Credential protection and cache file handling need review before use.

Mitigation: Before supplying a paid API key, request HTTPS-only approved destinations, safe redirect handling, and contained cache filenames; prefer protected local credential configuration over pasting keys into chat.

Risk: Searches send terms to PatentMax and may incur disclosed charges.

Mitigation: Use broad public terms and set a spending limit.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ip930/skills/patent-grant-time)
- [PatentMax API reference](artifact/references/api-reference.md)
- [Patent timing workflow and limitations](artifact/SKILL.md)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [Text, CSV]

**Output Format:** [Conversational summary and UTF-8-with-BOM CSV file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CSV includes filing-to-grant statistics and a patent sample list; estimates describe historical Chinese invention-patent grants, not individual outcomes.]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
