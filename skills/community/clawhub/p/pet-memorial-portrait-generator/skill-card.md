## Description: <br>
Create heartfelt pet memorial portraits and remembrance keepsakes for dogs, cats, and beloved animals who have passed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create pet memorial portrait prompts and request generated remembrance images through the Neta AI image generation API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the user's prompt, optional reference image identifier, and Neta/TalesOfAI token to api.talesofai.com. <br>
Mitigation: Avoid highly private memorial details and use a limited or disposable API token when possible. <br>
Risk: The documented usage passes the Neta/TalesOfAI token on the command line. <br>
Mitigation: Prefer a limited token and avoid sharing command history or terminal logs that include the token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/pet-memorial-portrait-generator) <br>
- [Neta API token setup](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text image URL with command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports portrait, landscape, square, and tall image sizes plus an optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
