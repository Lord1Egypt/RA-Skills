## Description: <br>
Converts dates between the Chinese lunar calendar and the Gregorian calendar using a local Python script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jincan0412](https://clawhub.ai/user/jincan0412) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to answer Chinese lunar-to-Gregorian and Gregorian-to-lunar date conversion requests, including birthday and calendar date lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python script and depends on the lunardate package. <br>
Mitigation: Install only after confirming local script execution is acceptable and the environment provides the disclosed dependency. <br>
Risk: Conversions are limited to the 1900-2100 date range documented by the artifact. <br>
Mitigation: Validate requested dates before relying on results and treat out-of-range or error responses as non-results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jincan0412/lunar-converter) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; script output is JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The conversion script returns a JSON object with a result string.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
