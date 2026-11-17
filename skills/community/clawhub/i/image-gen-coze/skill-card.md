## Description:

Image Generation via Coze generates images from a single prompt using a configured Coze workflow with the Seedream 4.5 model, including parameter construction and result parsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noah-1106](https://clawhub.ai/user/noah-1106)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask an agent to submit image prompts to a configured Coze workflow, parse the returned image URL, and optionally save generated images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and the Coze API token are used for external API calls to a configurable endpoint.

Mitigation: Install only from a trusted Coze configuration source, pin the endpoint to an official HTTPS Coze domain, and protect the credential config file.

Risk: Returned image URLs may be downloaded before validation.

Mitigation: Validate returned image URLs before download or use, and save generated files only to expected workspace locations.

## Reference(s):

- [Coze Homepage](https://www.coze.cn)
- [ClawHub Skill Page](https://clawhub.ai/noah-1106/skills/image-gen-coze)

## Skill Output:

**Output Type(s):** [API Calls, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with JSON configuration, shell command examples, image URLs, and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a single text prompt, supports prompt-level aspect-ratio tags, and recommends a 30-second interval between requests.]

## Skill Version(s):

1.1.4 (source: server release metadata; artifact frontmatter lists 1.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
