## Description: <br>
Generate images by customizing a URL. Drop the URL into websites, presentations, PDFs, or anywhere that loads images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jverlee](https://clawhub.ai/user/jverlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content authors use this skill to create imglink.ai image URLs and embed them in websites, Markdown, presentations, PDFs, or other surfaces that load images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and optional API keys are placed in shareable external URLs sent to imglink.ai. <br>
Mitigation: Avoid confidential prompts, personal data, and long-lived or sensitive API keys in URLs that may be published, logged, cached, or shared. <br>
Risk: Generated image URLs are intended for embedding and may be cached or reused. <br>
Mitigation: Use anonymous mode for testing and only embed URLs whose prompts and outputs are suitable for the target audience. <br>


## Reference(s): <br>
- [ImgLink website](https://imglink.ai) <br>
- [ImgLink image endpoint example](https://imglink.ai/images?prompt=cat) <br>
- [ClawHub release page](https://clawhub.ai/jverlee/imglink) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with image URL strings and optional HTML image snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include prompt, width, height, version, model, and optional key query parameters for imglink.ai URLs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
