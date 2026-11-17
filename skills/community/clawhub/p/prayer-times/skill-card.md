## Description:

Get instant, accurate Islamic prayer times for any location worldwide.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clinicode](https://clawhub.ai/user/clinicode)

### License/Terms of Use:


## Use Case:

External users use this skill to check daily Islamic prayer times for a manually supplied or IP-detected location worldwide. It is useful for Muslims, travelers, expats, students, and business travelers who need local salah times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto-detecting location contacts ipapi.co and may expose approximate location information through the user's IP address.

Mitigation: Provide a city or country manually when possible instead of using auto-detection.

Risk: Prayer times depend on third-party location, geocoding, and prayer-time APIs being reachable and returning accurate data.

Mitigation: Review the displayed location before relying on the times, especially for misspelled or ambiguous city names.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clinicode/skills/prayer-times)
- [ipapi.co location endpoint](https://ipapi.co/json/)
- [OpenStreetMap Nominatim search endpoint](https://nominatim.openstreetmap.org/search)
- [Aladhan timings endpoint](https://api.aladhan.com/v1/timings)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text prayer-time results with command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Displays location, date, and Fajr, Sunrise, Dhuhr, Asr, Maghrib, and Isha times in 12-hour format.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
