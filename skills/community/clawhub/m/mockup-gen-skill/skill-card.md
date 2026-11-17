## Description:

Generates AI mockup images from text prompts using the Neta AI image generation API and returns a direct image URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wkl-nieta](https://clawhub.ai/user/wkl-nieta)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate product mockup images from text prompts, optionally selecting output size or a reference image, and receive an image URL for downstream use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and API tokens are transmitted to the external api.talesofai.cn service.

Mitigation: Install only from a trusted source or version, confirm that api.talesofai.cn is the intended Neta endpoint, use a low-scope revocable token, and avoid sensitive or confidential prompts.

Risk: This version requires passing the Neta token on the command line despite documenting NETA_TOKEN support.

Mitigation: Use a temporary low-scope token where possible and review token exposure in shell history, process listings, and logs before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wkl-nieta/skills/mockup-gen-skill)
- [Neta Open API and Token Page](https://www.neta.art/open/)
- [Neta Image Generation API Endpoint](https://api.talesofai.cn/v3/make_image)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text image URL with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token and sends the prompt to an external image generation service.]

## Skill Version(s):

1.8.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
