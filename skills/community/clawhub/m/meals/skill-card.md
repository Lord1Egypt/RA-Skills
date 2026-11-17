## Description:

Build a personal meal planning system with weekly plans, shopping lists, and dietary tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users can use this skill to have an agent organize weekly meals, generate shopping lists, and maintain meal preferences and ratings in local files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meal plans, dietary restrictions, household preferences, and ratings may contain personal data stored under ~/meals/.

Mitigation: Treat ~/meals/ as personal data: review contents before sharing, use appropriate local file permissions, and avoid adding sensitive health details that are not needed for meal planning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/meals)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files]

**Output Format:** [Markdown meal plans, shopping lists, preference files, and conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates user-directed files under ~/meals/ when the agent is asked to maintain the meal-planning workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
