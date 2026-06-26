## Description: <br>
Scores a named trade show against a company profile using Lensmor's API and returns an exhibit, attend, or skip recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weilun88313](https://clawhub.ai/user/weilun88313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
B2B event, marketing, and sales teams use this skill to evaluate whether a specific trade show merits exhibiting, attending, monitoring, or skipping. The skill returns a fit score, scoring breakdown, decision band, and recommendation based on Lensmor's event data and the user's company profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an external Lensmor service for event lookup and scoring, so event queries and company-profile-derived scoring may be processed outside the user's environment. <br>
Mitigation: Confirm organizational approval for using Lensmor before sending business context or event scoring requests. <br>
Risk: The skill requires LENSMOR_API_KEY for authenticated API access. <br>
Mitigation: Store the key in a secure environment variable and never paste or print the key in prompts, logs, or responses. <br>
Risk: Fit scores can influence budget and event-planning decisions. <br>
Mitigation: Use the returned score and recommendation as decision support, and review the source event, dates, edition, and business assumptions before committing spend. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/weilun88313/lensmor-event-fit-score) <br>
- [Lensmor API Documentation](https://api.lensmor.com/) <br>
- [Lensmor Platform](https://platform.lensmor.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown score card with a score table, decision band, recommendation, and follow-up suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scores and breakdown values must come directly from the Lensmor API response; the skill requires LENSMOR_API_KEY.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
