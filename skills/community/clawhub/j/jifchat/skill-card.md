## Description:

Generate images and videos on the user's JifChat infinite canvas (jif.dev). Use when the user asks to generate, create, or render an image, product shot, poster, or short video with JifChat, or says "/jifchat", "/generate image", "/generate video", or "make a similar UGC video". Results land in a JifChat canvas project and spend the user's JifChat credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jifchat](https://clawhub.ai/user/jifchat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use the skill to create image and short-video generation projects on their JifChat canvas from text prompts and uploaded media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports that declining a paid video run may delete the project.

Mitigation: Confirm this behavior is removed or explicitly accepted before use, and preserve project work if the user declines.

Risk: The security review covered only 2 of 3 components and could not fully assess obfuscated instruction text.

Mitigation: Request complete component coverage and review obscured text before installation.

Risk: ClawScan guidance flags file-overwrite and reference-image privacy concerns.

Mitigation: Check file replacement behavior and avoid uploading sensitive reference images until their handling is clear.

## Reference(s):

- [JifChat Canvas](https://chat.jif.dev)
- [Character Consistency Guide](artifact/references/character-consistency.md)
- [One-Shot Example](artifact/references/one-shot.md)
- [JifChat Skill Page](https://clawhub.ai/jifchat/skills/jifchat)

## Skill Output:

**Output Type(s):** [Images, Videos, Canvas project content]

**Output Format:** [Generated image and video media in a JifChat canvas project]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation spends the user's JifChat credits.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
