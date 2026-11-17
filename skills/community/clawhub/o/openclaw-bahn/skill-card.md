## Description:

A comprehensive suite of commands for tracking Deutsche Bahn trains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ableitung](https://clawhub.ai/user/ableitung)

### License/Terms of Use:


## Use Case:

External travelers and developers use this skill to search stations, review departures, plan journeys, parse shared Deutsche Bahn itineraries, check live transfer status, and estimate transfer or Zugbindung risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts DB-related external services when retrieving live departures, journeys, delay data, and historical statistics.

Mitigation: Review network use before installing or running the skill in restricted environments.

Risk: Parsed travel plans may be retained locally, and the package includes a dated itinerary file.

Mitigation: Remove bundled or generated active.json files that should not be retained or shared.

Risk: Node package installs without pinned versions may reduce deployment reproducibility.

Mitigation: Pin and audit dependencies before managed or commercial deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ableitung/skills/openclaw-bahn)
- [Project Homepage](https://github.com/ableitung/openclaw-bahn)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [CLI text or structured JSON envelope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [All modes support --json; prediction and historical statistics are opt-in.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
