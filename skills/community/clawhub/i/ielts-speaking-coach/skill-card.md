## Description:

IELTS Speaking Coach helps learners practice IELTS Speaking, score text or audio responses across FC, LR, GRA, and PR bands, and receive corrections, model answers, and learning-path guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevin0818-lxd](https://clawhub.ai/user/kevin0818-lxd)

### License/Terms of Use:

MIT-0

## Use Case:

Learners and instructors use this skill to run IELTS Speaking practice, mock exams, band-score reviews, pronunciation checks, grammar corrections, vocabulary upgrades, and personalized study planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: IELTS answers and voice recordings may be processed through ASR and LLM workflows.

Mitigation: Use text-only mode for sensitive material and confirm whether the runtime stores transcripts or learning history before sending audio.

Risk: Broad IELTS-related activation can keep the assistant in IELTS mode longer than intended.

Mitigation: Exit IELTS mode when finished and review scores, corrections, and study advice before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevin0818-lxd/skills/ielts-speaking-coach)
- [IELTS speaking scoring rubric](artifact/scoring-rubric.md)
- [Learning path reference](artifact/learning-path.md)
- [Pronunciation guide](artifact/pronunciation-guide.md)
- [2025 May-August cue cards](artifact/cue-cards-2025-may-aug.md)
- [Vocabulary map](artifact/vocab-map.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured Chinese/English text with band scores, feedback, corrections, cue cards, study plans, and model answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include IELTS band scores from 1-9 in 0.5 increments and pronunciation source labels for audio-tested or text-estimated PR scores.]

## Skill Version(s):

1.1.2 (source: server release evidence, artifact skill.yaml, artifact clawhub.json, and artifact CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
