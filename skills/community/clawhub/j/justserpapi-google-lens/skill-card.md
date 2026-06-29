## Description: <br>
Call GET /api/v1/google/lens for Google SERP Lens through Just Serp API with a publicly accessible image URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to query the Just Serp API Google Lens endpoint for visual matches, product matches, related links, and other image-search results from a supplied image URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Just Serp API credential. <br>
Mitigation: Provide JUST_SERP_API_KEY through the environment or the --api-key argument, and do not paste credential values into chat messages, screenshots, or logs. <br>
Risk: The security evidence verdict is suspicious. <br>
Mitigation: Review the skill before installation and run it only with explicit user-provided operation parameters and trusted execution settings. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/justserpapi/justserpapi-google-lens) <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_lens&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_lens&utm_content=project_link) <br>
- [Generated operations reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and a publicly accessible image URL; optional query parameters include country, language, product, visual_matches, and exact_matches.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
