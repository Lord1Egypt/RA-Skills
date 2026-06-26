## Description: <br>
Generates handmade plush toy and stuffed animal images from text prompts, with optional size and reference-image settings, using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate plush toy concept images, stuffed animal references, merch mockups, gift ideas, and character or pet plush designs from text prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image UUIDs, and the Neta API token are sent to api.talesofai.com. <br>
Mitigation: Avoid sensitive personal or proprietary prompts and use a limited token where possible. <br>
Risk: Passing the API token on the command line can expose it through shell history, process listings, logs, or shared automation. <br>
Mitigation: Run token-bearing commands only in trusted environments, avoid logging commands that include tokens, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/omactiengartelle/plush-toy-generator) <br>
- [Publisher profile](https://clawhub.ai/user/omactiengartelle) <br>
- [Neta API token setup](https://www.neta.art/open/) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Plain text URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a direct generated image URL after polling the Neta API; supports size selection and an optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
