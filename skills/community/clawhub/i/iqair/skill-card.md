## Description: <br>
Gets real-time air quality data from the IQAir API for a city, coordinate pair, or nearest detected city, and returns AQI with a quality level. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atesluks](https://clawhub.ai/user/atesluks) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to answer air-quality, pollution, and AQI questions for specific locations. It can also supplement weather answers with current air-quality conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends queried city, coordinate, or nearest-location requests to IQAir. <br>
Mitigation: Prefer explicit city or coordinate lookups when privacy matters, and avoid --nearest unless IP-based location inference is acceptable. <br>
Risk: The skill requires an IQAir API key. <br>
Mitigation: Use a limited IQAir API key and store it only in the IQAIR_API_KEY environment variable. <br>


## Reference(s): <br>
- [IQAir API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/atesluks/iqair) <br>
- [Project Homepage](https://github.com/atesluks/openclaw-skill-iqair) <br>
- [IQAir API Key Dashboard](https://dashboard.iqair.com/personal/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text AQI summary, with Markdown guidance and inline shell commands when setup is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IQAIR_API_KEY and sends city, coordinate, or nearest-location requests to IQAir.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
