## Description:

Multimodal Gen helps agents structure text-to-image, image-to-image, text-to-video, image-to-video, and speech-to-text requests, including prompt-building guidance and helper scripts for ImageGen and VideoGen workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and agent operators use this skill to turn brief multimodal content requests into structured prompts and invocation guidance for image, video, and authorized audio transcription workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional learner can store local preference, failure, and note data in learned_patterns.json.

Mitigation: Avoid recording sensitive prompts, personal data, secrets, or confidential business context, and manage the file's retention and access controls.

Risk: Generated media or transcription workflows can raise copyright, impersonation, unlawful-content, or consent issues.

Mitigation: Follow the skill's safety boundaries: avoid infringing, illegal, sexual, or false-person portrait content; confirm rights for commercial materials; and process only authorized audio.

Risk: Image and video generation can consume paid credits.

Mitigation: Inform users of expected credit use before generation and validate video outputs with short durations before producing longer clips.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/multimodal-gen)
- [Publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured prompt text; helper scripts can print JSON-prefixed prompt data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local learned_patterns.json file when the optional learner script is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
