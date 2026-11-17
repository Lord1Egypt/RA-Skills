## Description:

PixelLab (pixellab.ai). Use this skill for ANY PixelLab request — reading, creating, updating, and deleting data. Whenever a task involves PixelLab, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and artists use PixelLab to generate, convert, edit, animate, and manage pixel-art images, characters, objects, and game UI assets through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified downloaded code.

Mitigation: Review setup and install a reviewed, fixed oo CLI release separately.

Risk: CLI setup may install or refresh persistent agent skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before CLI use to prevent skill synchronization.

Risk: PixelLab write and delete actions can change or remove saved assets.

Mitigation: Keep approval for writes and deletions, and confirm the exact target and effect before acting.

Risk: Requests pass through OOMOL and PixelLab and may consume credits.

Mitigation: Only send content acceptable to both services and check expected credit use before generation.

## Reference(s):

- [PixelLab](https://www.pixellab.ai/)
- [PixelLab API documentation](https://api.pixellab.ai/v2/docs)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Images, Files, API Calls, Text]

**Output Format:** [Pixel-art images and animation frames, with structured JSON results and file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may create or update saved PixelLab assets; generated content may consume credits.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
