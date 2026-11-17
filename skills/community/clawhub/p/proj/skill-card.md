## Description:

Explain, compare, and choose geographic coordinate reference systems and map projections, including CRS selection, EPSG codes, datum differences, axis order, units, and reprojection planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and GIS practitioners use this skill to choose, compare, and explain CRS and projection options for storage, web maps, measurement, analysis, and coordinate conversion planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implicit invocation could apply the skill to unrelated mapping, location, routing, or place-search tasks.

Mitigation: Use it only for coordinate-system, EPSG, datum, projection, axis-order, unit, or reprojection-planning questions.

Risk: Incorrect CRS assumptions can lead to misleading measurement or alignment guidance.

Mitigation: Confirm the source CRS, target CRS, units, datum, axis order, and whether a local transformation model is required before using the recommendation.

## Reference(s):

- [Common Coordinate Systems](references/common-systems.md)
- [ClawHub skill page](https://clawhub.ai/jvy/skills/proj)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline CRS identifiers, conversion recommendations, and handoff instructions when execution is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include EPSG codes, CRS names, axis-order warnings, unit notes, and references to related GIS execution skills.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
