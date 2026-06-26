## Description: <br>
Gets Islamic prayer times for locations worldwide, using IP-based auto-detection or city lookup to show Fajr, Sunrise, Dhuhr, Asr, Maghrib, and Isha in 12-hour format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clinicode](https://clawhub.ai/user/clinicode) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve daily salah times for a detected or requested location worldwide. It is useful for Muslims, travelers, and assistants that need current prayer-time lookup output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic location detection contacts a third-party IP geolocation service and can disclose approximate location information. <br>
Mitigation: Provide a city manually when privacy matters and install only if third-party location lookups are acceptable. <br>
Risk: Prayer-time lookup depends on third-party geocoding and prayer-time APIs for availability and returned results. <br>
Mitigation: Review the displayed location and prayer times before relying on the output, especially for travel or time-sensitive use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clinicode/prayer-times) <br>
- [ipapi IP geolocation endpoint](https://ipapi.co/json/) <br>
- [OpenStreetMap Nominatim search endpoint](https://nominatim.openstreetmap.org/search) <br>
- [Aladhan prayer timings endpoint](https://api.aladhan.com/v1/timings) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Displays a dated 12-hour table for Fajr, Sunrise, Dhuhr, Asr, Maghrib, and Isha.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
