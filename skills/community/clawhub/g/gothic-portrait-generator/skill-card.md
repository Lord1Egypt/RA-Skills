## Description: <br>
Generate gothic portraits with dark dramatic lighting, Victorian elegance, and moody atmosphere from text prompts using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate gothic, dark fantasy, Victorian-style, or dark academia portrait images from prompts, with optional size selection and reference-image style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference image UUIDs, and the Neta/TalesOfAI API token are sent to an external service. <br>
Mitigation: Avoid sensitive personal, proprietary, or regulated content and use the skill only when sharing that data with api.talesofai.com is acceptable. <br>
Risk: Passing the API token with the documented --token flag may expose it in shell history, process listings, or logs. <br>
Mitigation: Use a limited-use token and remove or protect command history and logs that may contain the token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/gothic-portrait-generator) <br>
- [Publisher profile](https://clawhub.ai/user/omactiengartelle) <br>
- [Neta API token setup](https://www.neta.art/open/) <br>
- [Image generation endpoint](https://api.talesofai.com/v3/make_image) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text, Guidance] <br>
**Output Format:** [Plain text image URL with command-line status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token, sends prompt and optional reference image UUID to api.talesofai.com, and supports portrait, landscape, square, and tall image sizes.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
