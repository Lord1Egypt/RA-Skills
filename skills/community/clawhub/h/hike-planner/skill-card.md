## Description:

Hike Planner helps agents create user-requested hiking trip plans with routes, transportation, lodging, local context, equipment lists, GPX/KML track analysis, and map links without booking, ordering, waitlisting, or paying.

This skill is ready for commercial/non-commercial use.

## Publisher:

[updatedb](https://clawhub.ai/user/updatedb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to plan hiking-oriented trips after the user provides dates, destination, and activity type. It can maintain local trip state, import GPX/KML tracks, generate itinerary Markdown, and update plans from user-provided travel details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores detailed trip, order, media, and GPS data locally.

Mitigation: Use a private output directory with appropriate file permissions, especially on shared systems.

Risk: Map and query workflows can send station names, destination details, or precise GPS coordinates to third-party services.

Mitigation: Review map-generation requests before use and avoid importing or sharing tracks that reveal sensitive locations.

Risk: Generated map HTML may expose embedded route coordinates if published or served broadly.

Mitigation: Keep generated map files local or access-controlled and do not expose them on public web servers.

Risk: Security evidence reports possible command execution or writes outside the intended trip folder in edge cases.

Mitigation: Review before installing and fix shell-command and path-boundary issues before use in shared or high-trust environments.

Risk: Optional helper skills and imported GPX/KML or media files can expand trust and input-handling risk.

Mitigation: Install helper skills only from trusted publishers and versions, and avoid importing untrusted GPX/KML or media files.

## Reference(s):

- [Hike Planner SOP](references/hike-planner-sop.md)
- [Plan Template](references/PLAN_TEMPLATE.md)
- [ClawHub Skill Page](https://clawhub.ai/updatedb/skills/hike-planner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown itinerary plans, JSON trip state, generated HTML map files, and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write trip plans, state files, imported media, GPX/KML copies, and track-map HTML under the configured output directory.]

## Skill Version(s):

3.3.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
