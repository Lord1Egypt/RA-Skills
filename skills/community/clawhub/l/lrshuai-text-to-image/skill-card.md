## Description: <br>
Generates images from text prompts by calling supported remote image-generation models through a Python helper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrshu](https://clawhub.ai/user/lrshu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to submit text prompts to supported image-generation models and receive generated image results through the configured service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the API key and prompt content to a configurable remote endpoint. <br>
Mitigation: Use a limited TEAM_API_KEY and verify that TEAM_BASE_URL is unset or points to a trusted service before running it. <br>
Risk: Local image or video inputs can be encoded and uploaded when optional media arguments are used. <br>
Mitigation: Do not pass local images or videos unless the user intends to upload that content to the configured service. <br>
Risk: The artifact asks the agent to run the Python helper directly instead of using the standard runner. <br>
Mitigation: Review the script before installing or executing the skill and prefer a release that explains why direct Python execution is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lrshu/lrshuai-text-to-image) <br>
- [Publisher profile](https://clawhub.ai/user/lrshu) <br>
- [Default remote model API endpoint](https://dlazy.com/api/ai/tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands] <br>
**Output Format:** [Console text and JSON returned from the remote image-generation API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and TEAM_API_KEY; TEAM_BASE_URL can override the default remote endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
