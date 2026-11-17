## Description:

Your personal AI stylist. Suggests an Outfit Of The Day based on real-time weather and your personal style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heytedward](https://clawhub.ai/user/heytedward)

### License/Terms of Use:


## Use Case:

External users use OOTD to get daily outfit recommendations that account for live weather, their local style profile, and an optional wardrobe file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal style or wardrobe details in USER.md or wardrobe.json may be used to personalize recommendations.

Mitigation: Keep sensitive information out of USER.md and wardrobe.json beyond what should be used for outfit advice.

Risk: Recommendations depend on live weather and local profile inputs, so inaccurate or stale inputs may produce unsuitable outfit advice.

Mitigation: Review the weather context and recommendation before acting on it, especially for severe or rapidly changing conditions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/heytedward/skills/ootd)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary with temperature, sky, vibe, and recommendation fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live weather, USER.md style preferences, and optional wardrobe.json items when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
