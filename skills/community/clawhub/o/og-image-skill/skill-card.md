## Description: <br>
Generate open graph social media preview images from text prompts using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sherrihidalgolt](https://clawhub.ai/user/sherrihidalgolt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to generate social preview and open graph images from prompts, with optional size selection and reference-image style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts, optional reference image UUIDs, and the user-provided API token are sent to api.talesofai.com. <br>
Mitigation: Use a dedicated revocable token, avoid confidential prompts, and avoid exposing real tokens in saved shell history or shared logs. <br>
Risk: The skill depends on an external image generation service and returns externally hosted image URLs. <br>
Mitigation: Review generated images and destination URLs before publication or downstream use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sherrihidalgolt/og-image-skill) <br>
- [Neta AI API access](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text image URL printed to stdout, with shell command examples in the skill documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Neta API token and may use an optional reference image UUID.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
