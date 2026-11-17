## Description:

Monitors live status for a Pod Point charging pod's A and B connectors, reporting current availability or changes without authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoranjurcevic](https://clawhub.ai/user/zoranjurcevic)

### License/Terms of Use:


## Use Case:

Drivers and agents use this skill to check a known Pod Point pod ID or wait for connector availability changes. It is focused on live charger availability, not charger discovery, maps, or location search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Watching a charger can run polling loops against a public status endpoint if broad interval or timeout values are allowed.

Mitigation: Use explicit pod IDs and enforce finite, sensible interval and timeout limits before long watch runs.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Structured JSON result with human-facing status or notification text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return current connector status, availability booleans, transition events, timeout status, and errors.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
