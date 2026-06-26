## Description: <br>
Provides Vietnamese lunar calendar lookup and conversion for solar dates, lunar dates, Can Chi, Vietnamese zodiac, auspicious hours, and solar terms using GMT+7 calendar rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuanxt](https://clawhub.ai/user/tuanxt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer Vietnamese lunar-calendar questions, convert between solar and lunar dates, and explain Can Chi, Vietnamese zodiac, auspicious hours, and solar terms without relying on model memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Node.js calendar calculator when answering Vietnamese lunar-date questions. <br>
Mitigation: Install only when local command execution for this purpose is acceptable, review the included scripts, and use the provided lockfile to keep dependency versions fixed. <br>
Risk: Lunar-to-solar reverse conversions and fortune or day-quality guidance may be approximate or culturally contextual. <br>
Mitigation: Present reverse conversions and fortune guidance as informational, and avoid using them as the sole basis for important decisions. <br>


## Reference(s): <br>
- [Lunar Calendar Vietnam ClawHub listing](https://clawhub.ai/tuanxt/lunar-calendar-vietnam) <br>
- [Vietnamese Almanac Fortune Rules](references/fortune_rules.md) <br>
- [24 Solar Terms Reference](references/solar_terms.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON data interpreted as concise natural-language guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Node.js command output for date calculations; fortune and day-quality advice is informational.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
