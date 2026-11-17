## Description:

Helps an agent plan and run a short multi-shot video sequence in one Runware video call, using model-specific shot templates, timing, continuity clauses, and optional anchor frames.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and video-generation operators use this skill to turn a brief with two to six story beats into one coherent multi-shot reel. It guides model selection, prompt structure, timing, anchor-frame use, asynchronous execution, and result checks for Runware video models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video prompts and anchor images may be processed by external video providers through Runware.

Mitigation: Avoid confidential, personal, copyrighted, or otherwise sensitive assets unless authorized to send them to that service.

Risk: Generated videos can miss intended cuts or drift from the requested subject identity across shots.

Mitigation: Review the resulting videoURL output for cut count, subject continuity, and anchor-frame fidelity before using or publishing the reel.

## Reference(s):

- [Multi-shot video worked recipes](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/runware/skills/multi-shot-video)

## Skill Output:

**Output Type(s):** [guidance, code, configuration, API calls]

**Output Format:** [Markdown with JSON request examples and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model-specific prompt templates, timing budgets, anchor-frame settings, asynchronous polling guidance, and video result review criteria.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
