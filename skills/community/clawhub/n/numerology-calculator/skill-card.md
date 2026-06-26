## Description: <br>
Calculate comprehensive numerology reports using Pythagorean or Chaldean systems, with support for English, Tamil, Telugu, Kannada, and Hindi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request numerology readings, life path and destiny numbers, name analysis, birth date numerology, and lucky number calculations through the ToolWeb API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends names and birth dates to ToolWeb for numerology processing. <br>
Mitigation: Use the skill only when the user is comfortable transmitting that data to ToolWeb, and avoid submitting personal data for anyone who has not agreed to that external transmission. <br>
Risk: The skill requires a ToolWeb API key and successful calls may consume free or paid quota. <br>
Mitigation: Configure TOOLWEB_API_KEY deliberately, monitor usage, and avoid unnecessary retries or calls without user intent. <br>
Risk: The skill depends on an external API and cannot produce the claimed proprietary numerology analysis when the API is unavailable. <br>
Mitigation: Surface API errors to the user and do not substitute unsupported numerology assessments from general model knowledge. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/numerology-calculator) <br>
- [ToolWeb API portal](https://portal.toolweb.in) <br>
- [Numerology API endpoint](https://portal.toolweb.in/apis/lifestyle/numerology) <br>
- [ToolWeb platform](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with curl command examples and API response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; sends names and birth dates to ToolWeb for numerology processing.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
