## Description:

Plans nearby places for dining, desserts, cafes, malls, cinemas, and date spots by combining structured POI recall, local search evidence, scoring, and fallback area guidance when store-level evidence is weak.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccmxigua](https://clawhub.ai/user/ccmxigua)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to plan local place recommendations with constraints such as origin, transit access, seating, category, budget, mall preference, and avoid rules. It returns a ranked recommendation with backups, weak-evidence notes, and next-step guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send addresses, coordinates, nearby-search terms, and possibly public IP information to external location and search providers.

Mitigation: Use an explicit origin when possible, avoid automatic nearby/current-location mode when IP privacy matters, and disclose that external providers may receive location-related inputs.

Risk: The skill depends on a sibling unified-search skill and its configured providers for evidence enrichment.

Mitigation: Review and install the unified-search dependency separately, verify its provider configuration, and treat weak or missing enrichment as uncertainty rather than a confirmed recommendation.

Risk: Some venue attributes, such as cinema screen types, may not be available in the primary POI source.

Mitigation: Use the documented secondary source path for specialty venue checks and keep uncertainty visible when store-level evidence is weak.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ccmxigua/skills/local-poi-planner)
- [Unified Search Suite dependency](https://clawhub.ai/ccmxigua/unified-search-suite)
- [Output template](artifact/references/output-template.md)
- [Lessons / 2026-05-31](artifact/references/lessons-2026-05-31.md)
- [Lessons / 2026-06-01](artifact/references/lessons-2026-06-01.md)
- [Amap Web Service API typecode reference](https://lbs.amap.com/api/webservice/download)
- [Maoyan cinema list endpoint](https://m.maoyan.com/ajax/cinemaList)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown recommendation report or JSON planner result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write intermediate JSON and rendered Markdown reports under /tmp/local-poi-planner-*.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
