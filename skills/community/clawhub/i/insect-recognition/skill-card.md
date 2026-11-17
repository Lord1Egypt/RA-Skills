## Description:

Identifies insects or other arthropods from an image URL or Base64-encoded image data, including names or taxonomy such as order, family, genus, or species.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit insect or arthropod images for recognition through a Xiaobenyang API-backed workflow. It is useful when a user needs a concise identification result from either an image URL or Base64 image input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images are submitted to an external Xiaobenyang API for recognition.

Mitigation: Use the skill only when the API provider is trusted for the submitted images and its privacy terms are acceptable.

Risk: The API key is written to a local plaintext .env file.

Mitigation: Keep .env out of repositories and backups, restrict local file access, and rotate the key after testing or suspected exposure.

Risk: Configuration drift in the package requires review before installation.

Mitigation: Review the skill instructions and configuration before deployment, especially API key handling and the selected Xiaobenyang tool endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/insect-recognition)
- [Xiaobenyang API key portal](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Markdown summary of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an API key and either an image URL or Base64-encoded image data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
