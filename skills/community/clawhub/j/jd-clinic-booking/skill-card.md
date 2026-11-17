## Description:

Jd helps users view JD Clinic booking guidance, submit appointment requests, contact support, check prices, and find app download links for a dermatology clinic in Seoul.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beautsgo](https://clawhub.ai/user/beautsgo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get JD Clinic appointment guidance, submit booking requests through BeautsGO, contact clinic support, and look up treatment prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Appointment details and an optional phone number may be sent to BeautsGO/yestokr services.

Mitigation: Review before installing and use only if users are comfortable sending those details to the listed services.

Risk: The security review reports embedded API tokens.

Mitigation: The publisher should rotate exposed API tokens before release or deployment.

Risk: The security review reports URL opening through a shell.

Mitigation: The publisher should replace shell URL opening with argument-based process launch.

Risk: The skill promotes a direct APK download that lacks a trusted checksum or store-based installation path.

Mitigation: Prefer store-based installation links or require the publisher to provide a trusted checksum before using the APK link.

Risk: Appointment requests can be submitted after information is parsed from user input.

Mitigation: Add an explicit booking confirmation step before sending appointment data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beautsgo/skills/jd-clinic-booking)
- [BeautsGO JD Clinic booking page](https://i.beautsgo.com/cn/hospital/jd-clinic/skill)
- [BeautsGO JD Clinic detail page](https://i.beautsgo.com/cn/hospital/jd-clinic?from=skill)
- [BeautsGO website](https://www.beautsgo.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-formatted string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include booking guidance, appointment submission results, price lookup results, support links, clinic page links, and app download links.]

## Skill Version(s):

1.0.0 (source: release metadata, SKILL.md frontmatter, package.json, and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
