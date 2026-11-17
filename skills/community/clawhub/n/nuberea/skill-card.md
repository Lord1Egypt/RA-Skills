## Description:

Nuberea lets agents query Bible research datasets covering Hebrew and Greek morphology, lexicons, KJV text, Dead Sea Scrolls, New Testament manuscript transcriptions, Septuagint data, synoptic parallels, and SQL analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[streamsapps](https://clawhub.ai/user/streamsapps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and advanced Bible study users use Nuberea to retrieve scripture, morphology, lexicon, manuscript, and synoptic-parallel evidence through typed tools or read-only SQL over the provided research datasets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Freeform SQL queries can produce overly broad, expensive, or misleading cross-table analysis if used for routine lookups.

Mitigation: Prefer typed lookup and search tools for routine study, and use SQL only for intentional cross-table analysis over the provided read-only datasets.

## Reference(s):

- [NuBerea MCP Tools Reference](artifact/references/tools.md)
- [ClawHub skill page](https://clawhub.ai/streamsapps/skills/nuberea)

## Skill Output:

**Output Type(s):** [Text, Structured data, Analysis]

**Output Format:** [Tool responses from typed lookups, searches, and read-only SQL queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public or research Bible text, morphology, lexicon, manuscript, and cross-reference query results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
