## Description:

Helps turn a reference short video into a new, editable production with analysis, scripts, captions, optional generated shots, and a locally rendered MP4.

This skill is ready for commercial/non-commercial use.

## Publisher:

[narcooo](https://clawhub.ai/user/narcooo)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and marketing teams use this skill to analyze a reference short, plan an original adaptation, and deliver an editable video project and finished MP4. Local editing works without model generation; generated shots use the user's separately billed APIsRouter account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional model generation can incur charges on the user's APIsRouter account.

Mitigation: Review current pricing and the number and specifications of planned requests, and obtain authorization before submitting paid jobs.

Risk: Local media and an optional APIsRouter API key may contain sensitive user material.

Mitigation: Use the host secret facility for the API key, keep it out of chat and shared projects, and share local media only within the user's intended scope.

Risk: Generation job receipts may contain signed result URLs.

Mitigation: Keep receipt files private and omit signed URLs from shared deliverables.

## Reference(s):

- [ClawHub release](https://clawhub.ai/narcooo/skills/hype-shorts-remix)
- [APIsRouter](https://apisrouter.com)
- [Creative workflow](references/workflow.md)
- [Generation guide](references/generation.md)
- [Edit format](references/edit-format.md)
- [Setup guide](references/setup.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON configuration, Video (MP4)]

**Output Format:** [Reference analysis, script and shot plan in Markdown; editable JSON project; rendered MP4]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is optional and billed separately; local rendering produces a media report.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
