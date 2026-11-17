## Description:

Designs 9:16 talking-head reel motion graphics by using a frame capture to place overlays in safe zones, classifying the transcript into overlay types, and producing transparent PNG cards, a motion board, and an editor assembly sheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, and agent operators use this skill to plan and generate motion-graphic overlays for vertical talking-head reels. It helps classify caption content, choose overlay templates, define safe placement, and package PNG cards with timing and placement instructions for a video editor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run shell commands and install or relink system tools.

Mitigation: Run it in a contained environment and require explicit approval before installing packages, relinking tools, rendering, cutting, or composing video.

Risk: The skill may read a local secret file and use a transcript API key.

Mitigation: Provide secrets through environment variables where possible and avoid writing API keys into files, logs, or generated outputs.

Risk: Remote video URLs may be sent to Supadata for transcription.

Mitigation: Confirm the user has permission to process the video URL and approve third-party transcript calls before sending any URL.

Risk: The artifact contains conflicting behavior about final video editing or rendering.

Mitigation: Treat this release as producing PNG overlays, motion_board.json, and HOJA_MONTAJE.md only; review any request to cut, render, or compose final video separately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/motion-reels-f100k)
- [Publisher profile](https://clawhub.ai/user/formula100k)
- [Supadata transcript API](https://api.supadata.ai/v1/transcript)
- [GSAP CDN script](https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with shell commands, HTML/GSAP snippets, JSON motion-board data, transparent PNG assets, and a Markdown assembly sheet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets 1080x1920 vertical reels and does not compose the final video in this agent release.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
