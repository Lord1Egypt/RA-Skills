## Description:

Generates a shareable 2026 Year of the Horse New Year fortune video, with HTML used only as an intermediate screenshot and preview asset.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weiweidesigner](https://clawhub.ai/user/weiweidesigner)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to generate personalized New Year fortune videos from user-provided name, gender, birth details, personality, and wishes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal details may be sent to external AI services without sufficient disclosure.

Mitigation: Use only with clear consent and avoid real names, exact birth details, birthplace, and private wishes unless disclosure and data controls are added.

Risk: The security review reports hardcoded credentials and disabled TLS verification.

Mitigation: Require the publisher to remove embedded credentials, use user-supplied secrets, and restore standard TLS certificate verification before trusted use.

Risk: The skill may install packages or browser drivers at runtime and modify the local environment.

Mitigation: Run only in an isolated disposable environment until runtime downloads are removed and dependencies are pinned and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weiweidesigner/skills/happynewyear)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [MP4 video file with an intermediate HTML preview and JSON status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The primary output is new_year_blessing_video.mp4; new_year_blessing.html is an intermediate preview asset.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
