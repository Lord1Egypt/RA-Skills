## Description:

Store source-linked entities and relationships, traverse their connections and export a local graph. Use for Entity Relationship Memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and developers use this skill to keep source-linked records of entities and relationships, inspect connected records, and export a graph for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored relationships and exported reports remain on disk without application-level encryption.

Mitigation: Use authorized information, approve sensitive details before storage, and protect or remove the .mochilab/entity-graph/ and exports/entity-graph/ folders when appropriate.

## Reference(s):

- [Action contract](references/input.md)
- [ClawHub release](https://clawhub.ai/hznetnewpower/skills/mochi-entity-graph)

## Skill Output:

**Output Type(s):** [JSON, HTML, Files, Guidance]

**Output Format:** [JSON requests and operation responses, with local JSON and HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports contain source-linked entity and relationship records and are saved in the active workspace.]

## Skill Version(s):

1.0.1 (source: server-resolved release and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
