## Description:

Generates personalized learning paths from a learner's goals, current level, available time, preferences, and constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and learners use this skill to turn learning goals into structured roadmaps with phases, milestones, resource suggestions, progress checkpoints, recommendations, and next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unbounded or invalid timeframe values could produce unrealistic plans or make the skill unsuitable for public-service use.

Mitigation: Add runtime validation and reasonable bounds for total weeks, weekly hours, and deadlines before exposing the skill through an API or shared service.

Risk: The skill is Chinese-first, which may mismatch a user's preferred response language.

Mitigation: Clarify and honor the user's language preference when generating learning plans.

Risk: Resource recommendations are based on typical scenarios rather than live education-platform data.

Mitigation: Review recommended resources before relying on them and connect authoritative education-platform APIs when current availability or pricing matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/learning-path-navigator)
- [Publisher profile](https://clawhub.ai/user/harrylabsj)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or structured JSON-style learning path report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include phased plans, weekly checkpoints, resource recommendations, assessments, milestones, progress tracking, and next steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
