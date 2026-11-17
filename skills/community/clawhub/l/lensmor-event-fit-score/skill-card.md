## Description:

Scores a specific trade show against a company profile using the Lensmor API and returns an exhibit, attend, or skip recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weilun88313](https://clawhub.ai/user/weilun88313)

### License/Terms of Use:

MIT-0

## Use Case:

External B2B event, marketing, and revenue teams use this skill to get a quantified trade-show fit score before committing booth budget or travel spend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Lensmor API key.

Mitigation: Store LENSMOR_API_KEY as a secret and do not paste real tokens into prompts, screenshots, logs, or shared output.

Risk: Trade-show queries and Lensmor company-profile context may be sent to the Lensmor service to compute scores.

Mitigation: Install and use the skill only when external Lensmor API processing is intended and acceptable for the user's data.

Risk: Incorrect event selection can produce a misleading exhibit, attend, or skip decision.

Mitigation: Confirm the resolved event ID, year, and edition before requesting a fit score.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weilun88313/skills/lensmor-event-fit-score)
- [Lensmor API documentation](https://api.lensmor.com/)
- [Lensmor platform](https://platform.lensmor.com)
- [Lensmor website](https://www.lensmor.com/?utm_source=github&utm_medium=skill&utm_campaign=trade-show-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown score card with a decision band, score breakdown, recommendation, and follow-up suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores and breakdown values must come from the Lensmor API; the skill requires LENSMOR_API_KEY.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
