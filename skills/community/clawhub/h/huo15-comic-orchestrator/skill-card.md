## Description:

Huo15 Comic Orchestrator coordinates a multi-step AI comic-drama workflow from theme intake through script, character cards, storyboard frames, video generation, TTS, lip sync, background music, subtitles, and final assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to orchestrate short AI comic-drama production runs with cost checks, user confirmation, checkpoint resume, and handoff across required sibling skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media prompts and referenced assets may be sent to external providers.

Mitigation: Use only approved input content, review provider terms, and supervise each run.

Risk: Billing and dependency controls are too weak for unattended installation.

Mitigation: Avoid unattended or auto-confirmed use until dependencies are pinned and runtime spending is enforced from actual provider usage.

Risk: The workflow depends on required sibling skills and external provider credentials.

Mitigation: Install and pin the required sibling skills, configure provider credentials deliberately, and run in a controlled project directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-comic-orchestrator)
- [Volcengine Seedance documentation](https://www.volcengine.com/docs/82379/1520757)
- [Volcengine TTS documentation](https://www.volcengine.com/docs/6561/97465)
- [Kling API endpoint](https://api.klingai.com/v1)
- [Suno API endpoint](https://api.sunoapi.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance, command examples, JSON project state, media file paths, and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a final video path, cost report, and checkpointed project outputs when the required sibling skills and provider credentials are available.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
