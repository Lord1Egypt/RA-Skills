## Description:

Convert PowerPoint presentations into narrated videos with Simplified Chinese voiceover, synchronized subtitles, and page-by-page audio sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffli2002](https://clawhub.ai/user/jeffli2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to convert slide decks into narrated training, explainer, or course videos with page-by-page audio and subtitle synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering instructions use an unpinned npx Remotion command that can execute changing third-party code on the user's machine.

Mitigation: Pin Remotion in package.json with a lockfile and run the local executable in a sandboxed workspace without unnecessary credentials.

Risk: The skill is designed for Simplified Chinese voiceover and subtitles.

Mitigation: Use this skill only when Simplified Chinese output matches the intended video language.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeffli2002/skills/ppt2video)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent guidance for extracting slide images, generating per-slide audio, configuring a Remotion project, and rendering an MP4 video.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
