## Description: <br>
IELTS Speaking Coach acts as an IELTS speaking examiner and tutor that scores spoken English across FC, LR, GRA, and PR bands, supports audio-based pronunciation scoring, and provides practice, corrections, model answers, mock exams, and personalized learning paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevin0818-lxd](https://clawhub.ai/user/kevin0818-lxd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
IELTS learners use this skill to practice Parts 1, 2, and 3, receive IELTS-style band feedback, improve grammar and vocabulary, and run mock speaking exams. It can also guide tutors or coaches who want structured speaking prompts, scoring rubrics, and study-plan suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio messages, transcripts, and score data can be privacy-sensitive when sent to the configured LLM or ASR environment. <br>
Mitigation: Use text-only mode for higher privacy and avoid including sensitive personal details in practice answers. <br>
Risk: Optional persistent learning-state tracking can retain learner progress data when an external backend is enabled. <br>
Mitigation: Review and configure the optional backend separately before enabling persistence; the ClawHub package works without it. <br>
Risk: Audio pronunciation scoring depends on ffmpeg and ASR availability, so pronunciation output may fall back to estimation. <br>
Mitigation: Confirm ffmpeg and ASR are available for audio scoring, or clearly rely on the documented text-only PR estimate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kevin0818-lxd/ielts-speaking-coach) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [IELTS Speaking Band Descriptors](artifact/scoring-rubric.md) <br>
- [ZPD Learning Path Reference](artifact/learning-path.md) <br>
- [Pronunciation Guide](artifact/pronunciation-guide.md) <br>
- [Cue Cards 2025 May-August](artifact/cue-cards-2025-may-aug.md) <br>
- [Cue Cards](artifact/cue-cards.md) <br>
- [Assessment Examples](artifact/examples.md) <br>
- [Vocabulary Map](artifact/vocab-map.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown-style feedback with IELTS band scores, corrections, model answers, cue cards, mock-exam reports, and learning plans.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include IELTS band scores in 0.5 increments, pronunciation notes, Chinese or English feedback, and text-only fallback when audio tooling is unavailable.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata, artifact/clawhub.json, and artifact/skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
