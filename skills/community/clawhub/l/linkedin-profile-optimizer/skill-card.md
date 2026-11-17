## Description:

Audits and rewrites LinkedIn profile sections including the photo, banner, headline, About, Featured, Experience, Skills, custom URL, and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to review LinkedIn profile URLs, screenshots, or draft profile content and produce a prioritized profile audit with section rewrites for job seeking, client acquisition, or authority building.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated LinkedIn profile copy could overstate a user's credentials, results, or positioning if accepted without review.

Mitigation: Review all generated public-facing profile text before posting and verify that claims, metrics, and recommendations match the user's evidence.

Risk: Benchmark and uplift claims may be marketing guidance rather than independently verified performance guarantees.

Mitigation: Present expected-uplift language as directional context and avoid treating it as a guaranteed outcome.

Risk: Broad trigger wording could invoke the skill for profile-related requests that are not explicit audits or rewrites.

Mitigation: Use the skill when the user clearly asks for a LinkedIn profile audit, rewrite, or section optimization, and ask for the profile goal when unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sergebulaev/skills/linkedin-profile-optimizer)
- [Profile Headline Formulas](references/profile-headline-formulas.md)
- [About Section Templates](references/about-section-templates.md)
- [Featured Section Playbook](references/featured-section-playbook.md)
- [Banner & Photo Specs](references/banner-photo-specs.md)
- [Experience, Skills, Custom URL, Recommendations](references/experience-skills-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown audit with a scorecard, ranked fixes, before/after rewrites, and expected-uplift notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided profile URL, screenshots, or draft profile content; generated public profile text should be reviewed before posting.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
