## Description:

Translates text and text embedded in images or image URLs through the Xiangji/Tosoiot translation service, with support for batch image translation and multiple translation engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leoking](https://clawhub.ai/user/leoking)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to translate text, local images, or batches of image URLs between supported languages through Xiangji/Tosoiot APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API credentials for text and image translation.

Mitigation: Use approved credential handling and prefer adapting the scripts to read secrets from environment variables or a secure secret store rather than command-line flags.

Risk: The skill sends text, local images, and image URLs to Xiangji/Tosoiot translation services.

Mitigation: Use only content you are authorized to share, and avoid confidential, regulated, internal, personal, or signed image URL content unless policy and terms permit it.

## Reference(s):

- [Xiangji official website](https://www.xiangjifanyi.com/)
- [Xiangji OpenAPI documentation](https://openapi-doc.xiangjifanyi.com/)
- [Supported languages](references/languages.md)
- [Image Translator ClawHub listing](https://clawhub.ai/leoking/skills/image-translator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python script commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Xiangji/Tosoiot API credentials and sends text, images, or image URLs to external translation APIs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
