## Description:

Provides daily Islamic reflections with Hijri calendar awareness, Quran/Hadith references, and practical daily challenges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clinicode](https://clawhub.ai/user/clinicode)

### License/Terms of Use:


## Use Case:

External users ask for a daily Islamic reflection or reminder, and the skill returns a formatted reflection selected by Gregorian and Hijri calendar context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reflection script contacts api.aladhan.com to convert the current date to a Hijri date.

Mitigation: Disclose the third-party API request before installation or execution, and use the skill only where that outbound request is acceptable.

Risk: The skill can run for broad trigger phrases such as requests to be inspired or motivated.

Mitigation: Narrow invocation to explicit Islamic reflection requests before deployment in contexts where broad religious-content triggers are not desired.

Risk: The script depends on network access for the Hijri date and may fall back to an unknown date if the request fails.

Mitigation: Add or verify an offline Hijri-date fallback when date accuracy is important.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clinicode/skills/islamic-daily-reflection)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Formatted plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output includes a date line, reflection title, reflection text, daily action, and Quran or Hadith reference.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
