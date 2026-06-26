## Description: <br>
Generates royal Renaissance-style oil painting portraits of pets from text prompts using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate custom Renaissance-style pet portraits from text prompts, with optional size selection and reference image style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference UUIDs, and the Neta API token are sent to api.talesofai.com. <br>
Mitigation: Avoid sensitive personal details in prompts and use a limited-scope or short-lived token where possible. <br>
Risk: Passing the token on the command line may expose it through shell history or local process listings. <br>
Mitigation: Run the skill only in trusted environments, avoid shared systems for token-bearing commands, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [Neta AI Open](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text image URL on stdout, with progress and errors on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a text prompt and Neta API token; supports optional image size and reference image UUID parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
