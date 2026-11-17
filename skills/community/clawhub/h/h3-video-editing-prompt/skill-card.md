## Description:

Write or revise MiniMax H3 Ref2VA prompts for editing a source video from reference images or audio, especially masked or false-colour person replacement, face replacement, costume or object replacement, cross-shot identity persistence, overlay cleanup, and lip-sync preservation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangminrui2022](https://clawhub.ai/user/wangminrui2022)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video prompt authors use this skill to draft or revise MiniMax H3 Ref2VA editing prompts from supplied source video, reference image, and optional audio assets. It focuses on masked replacement, face or object replacement, cross-shot identity persistence, overlay cleanup, and realistic limits around lip sync and time-window control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prompts can imply more control than MiniMax H3 can guarantee for masks, untouched time ranges, cross-shot identity, or frame-accurate lip sync.

Mitigation: Inspect the provided assets, classify mask and audio conditions, state limits in the prompt, and use segmentation or dedicated lip-sync and face-reenactment stages when precision is required.

Risk: The skill may guide edits involving identifiable people or user-provided likeness references.

Mitigation: Use only media and reference assets that the operator is authorized to edit, and review generated prompts before sending them to a video model.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangminrui2022/skills/h3-video-editing-prompt)
- [Editing recipes](artifact/references/editing-recipes.md)
- [Universal replacement template](artifact/references/universal-replacement-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown containing a six-field Ref2VA prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is one English text block with subject_definitions, summary, retention_analysis, detailed_description, overall_soundscape, and non_diegetic_music; target length is about 7000 characters with a 10000-character maximum.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
