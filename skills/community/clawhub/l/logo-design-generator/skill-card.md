## Description: <br>
AI logo generator and logo design maker that creates professional brand logos, company emblems, startup icons, app logos, and business identity marks from text prompts via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate logo concepts and brand identity marks from text prompts, with optional size selection and reference-image style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logo prompts, reference image IDs, and the Neta API token are sent to the external Neta/TalesOfAI service. <br>
Mitigation: Avoid confidential business details or secrets in prompts, review the service terms before use, and only install if external API processing is acceptable. <br>
Risk: The documented --token CLI flag can expose the Neta API token through shell history or process listings. <br>
Mitigation: Treat the token as sensitive, avoid shared shells when invoking the command, and rotate or revoke the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/logo-design-generator) <br>
- [Neta AI API access](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls] <br>
**Output Format:** [Plain text image URL with command-line progress messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token, a text prompt, optional image size, and optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
