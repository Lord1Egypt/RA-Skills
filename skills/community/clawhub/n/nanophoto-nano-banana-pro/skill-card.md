## Description: <br>
Generate or edit AI images with the NanoPhoto.AI Nano Banana Pro API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanophotohq](https://clawhub.ai/user/nanophotohq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate images from prompts or edit images from public image URLs through NanoPhoto.AI, then return generation status and final image links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, public image URLs, and generation metadata are sent to the NanoPhoto service. <br>
Mitigation: Do not submit sensitive, private, regulated, or proprietary image content unless approved for third-party processing. <br>
Risk: The skill requires a NanoPhoto API key. <br>
Mitigation: Configure NANOPHOTO_API_KEY through the platform's secure environment setting and avoid entering keys directly in command-line arguments when possible. <br>
Risk: Edit mode operates on public image URLs supplied by the user. <br>
Mitigation: Use only image URLs you are authorized to process and are comfortable sending to NanoPhoto. <br>


## Reference(s): <br>
- [Nano Banana Pro Image Generation API Reference](references/api.md) <br>
- [NanoPhoto.AI homepage](https://nanophoto.ai) <br>
- [NanoPhoto API key settings](https://nanophoto.ai/settings/apikeys) <br>
- [ClawHub skill page](https://clawhub.ai/nanophotohq/nanophoto-nano-banana-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NANOPHOTO_API_KEY; edit mode accepts up to 8 public image URLs and polling may take 30-300 seconds.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
