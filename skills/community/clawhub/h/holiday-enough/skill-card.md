## Description:

Assesses whether a user's available vacation days are enough for a destination by gathering real travel-guide timing data and returning a concise adequacy judgment with supporting itinerary timing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrlyk](https://clawhub.ai/user/mrlyk)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to compare a destination against available holiday days, estimate recommended trip length from real user guides, and decide whether the schedule is generous, adequate, or tight.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires control over a Chrome instance with remote debugging enabled, which can expose more browser access than the travel-planning task requires.

Mitigation: Use an isolated temporary browser profile, restrict activity to pages opened for the task, and disable remote debugging after use.

Risk: The local CDP proxy exposes endpoints for arbitrary page evaluation, screenshots, and file input actions on reachable Chrome tabs.

Mitigation: Run the proxy only on localhost for the shortest necessary time, avoid using a primary browsing profile, and review each requested browser action before proceeding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrlyk/skills/holiday-enough)
- [Publisher profile](https://clawhub.ai/user/mrlyk)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with concise travel assessment sections and inline shell commands when setup is required]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recommended days, the user's available days, an adequacy rating, attraction timing evidence, and schedule adjustment suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
