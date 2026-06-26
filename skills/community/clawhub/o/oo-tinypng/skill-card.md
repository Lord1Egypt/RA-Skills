## Description: <br>
TinyPNG (tinypng.com) skill for operating TinyPNG through an OOMOL-connected account to shrink images and transform TinyPNG output images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to compress images from public URLs or base64 image bytes and to transform TinyPNG output images through an OOMOL-connected TinyPNG account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload or transform images through an OOMOL-connected TinyPNG account. <br>
Mitigation: Confirm the exact image URL or image bytes and intended transformation before running shrink_image or output_image. <br>
Risk: The security evidence says image upload and transformation actions are under-labeled as safe read-like operations. <br>
Mitigation: Treat shrink_image and output_image as mutating external-processing actions even when the artifact does not tag them as write actions. <br>
Risk: The skill requires a connected TinyPNG account and may encounter auth, connection, credential, or billing failures. <br>
Mitigation: Use setup or billing steps only after the connector command fails with the matching error. <br>


## Reference(s): <br>
- [ClawHub TinyPNG Skill](https://clawhub.ai/oomol/oo-tinypng) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [TinyPNG Homepage](https://tinypng.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema checks before constructing TinyPNG action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
