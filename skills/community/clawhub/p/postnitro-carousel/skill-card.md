## Description: <br>
Generates social media carousel posts through the PostNitro.ai Embed API using AI generation from text, article URLs, or X posts, or by importing user-authored slide content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iAmMuneeb](https://clawhub.ai/user/iAmMuneeb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, content teams, and developers use this skill to create LinkedIn, Instagram, TikTok, and X carousel assets from topics, articles, posts, or structured slide content. It is useful when an agent needs to produce carousel-generation instructions, request payloads, polling steps, and downloadable PNG or PDF output links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted text, article URLs, X post URLs, and slide content are sent to PostNitro. <br>
Mitigation: Do not submit private drafts, internal URLs, personal data, secrets, or regulated content unless authorized to share it with PostNitro. <br>
Risk: Carousel generation can spend PostNitro account credits. <br>
Mitigation: Confirm the intended generation method and expected credit cost before initiating API calls. <br>
Risk: The skill requires a PostNitro API key and account-specific template, brand, and preset identifiers. <br>
Mitigation: Use a scoped or dedicated API key where possible and confirm the target PostNitro account before use. <br>


## Reference(s): <br>
- [PostNitro Skill Listing](https://clawhub.ai/iAmMuneeb/postnitro-carousel) <br>
- [PostNitro](https://postnitro.ai) <br>
- [PostNitro Embed API Reference](artifact/references/api-reference.md) <br>
- [PostNitro Carousel Skill Examples](artifact/examples/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce PostNitro output URLs for PNG slide images or a PDF file after asynchronous API completion.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
