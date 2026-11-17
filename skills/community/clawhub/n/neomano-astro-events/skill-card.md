## Description:

Provides local astronomical visibility including moon phase, rise/set times, planet viewing windows, and optional ISS pass predictions by location and date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elandivar](https://clawhub.ai/user/elandivar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer location-specific astronomy visibility questions, including tonight's Moon phase, twilight window, planet viewing times, and ISS passes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup downloads Python packages and runs fetch public astronomy datasets from the network.

Mitigation: Install only in environments where those downloads are acceptable; stricter deployments should pin dependencies and use local dataset caches.

Risk: ISS predictions depend on current public TLE data and can be unavailable or stale when network access fails.

Mitigation: Review the report context before relying on predictions and consider an offline or no-ISS mode for constrained environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elandivar/skills/neomano-astro-events)
- [Celestrak ISS TLE dataset](https://celestrak.org/NORAD/elements/stations.txt)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text astronomy report with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are generated for a supplied latitude, longitude, timezone, and date window.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
