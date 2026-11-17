## Description:

Collects, stores, and manages internet-radio.com music stream records with auto-population, availability checks, adaptive speed thresholds, and related command-line database utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dynamicsalex](https://clawhub.ai/user/dynamicsalex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to build and maintain a local internet radio stream database, inspect stream health and genre statistics, and manage or export stream records for playback tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound requests to many radio-stream URLs, including arbitrary stream URLs stored in the local database.

Mitigation: Run it on networks where this egress is acceptable, add URL validation or network egress controls before scheduled use, and review sources before importing or adding streams.

Risk: Availability checks can modify state.json and remove streams after repeated failures.

Mitigation: Back up state.json before automated checks and review failed-check thresholds or outputs before relying on removals.

## Reference(s):

- [ClawHub skill homepage](https://clawhub.ai/skills/internet-radio-music-db)
- [Published skill page](https://clawhub.ai/dynamicsalex/skills/internet-radio-music-db)
- [internet-radio.com source catalog](https://www.internet-radio.com)
- [Internet Radio Music WebUI plugin](https://clawhub.ai/dynamicsAlex/internet-radio-music-webui)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON database records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create, update, remove, and export local stream records in state.json.]

## Skill Version(s):

2.6.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
