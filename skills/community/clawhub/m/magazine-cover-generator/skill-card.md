## Description:

Generate AI magazine cover art from text prompts in editorial styles such as Vogue, TIME, and GQ using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate magazine cover mockups, parody covers, personal branding images, social media posts, pet covers, and mixed-media editorial collage designs from text prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and optional reference image IDs are sent to api.talesofai.com.

Mitigation: Use only prompts and reference IDs that are acceptable to share with the third-party Neta API service.

Risk: The documented command passes the API token as a command-line argument, which can expose it locally through shell history or process listings.

Mitigation: Prefer a safer secret mechanism when adapting the script and avoid pasting real tokens into reusable shell commands.

Risk: The documented npx installer is unpinned.

Mitigation: Review or pin the installer source before using the install command in controlled environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/omactiengartelle/skills/magazine-cover-generator)
- [Neta API Token Setup](https://www.neta.art/open/)
- [Neta API Service](https://api.talesofai.com)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text image URL returned from a command-line invocation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports portrait, landscape, square, and tall sizes, plus an optional reference image UUID for style inheritance.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
