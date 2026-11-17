## Description:

MadStory helps creators plan cinematic storyboards and generation prompts for Seedance video and Seedream image workflows, including multi-shot, advertising, brand film, and short-drama modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, production teams, marketers, and short-drama teams use this skill to turn concepts, references, scripts, or product ideas into structured storyboard plans and generation-ready prompts. It is intended for cinematic video and image-generation planning rather than general static visual design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional HTML storyboard preview can expose a browser injection risk when rendering untrusted storyboard data.

Mitigation: Sanitize storyboard fields before preview rendering and avoid hosting generated previews in a privileged browser origin.

Risk: Voice, image, and video references may contain content that requires rights, consent, or identity-sensitive handling.

Mitigation: Use uploaded reference media only with appropriate rights and consent, and review outputs before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qomob/skills/madstory)
- [Publisher profile](https://clawhub.ai/user/qomob)
- [qomob.ai](https://qomob.ai)
- [Seedance 2.5 rules](artifact/references/seedance_25_rules.md)
- [Modes detail](artifact/references/modes_detail.md)
- [Phases detail](artifact/references/phases_detail.md)
- [Prompt engineering](artifact/references/prompt_engineering.md)
- [Seedance 2.0 rules](artifact/references/seedance_v2_rules.md)
- [Seedream rules](artifact/references/seedream_4x_rules.md)
- [Terminology](artifact/references/terminology.md)
- [Pre-flight checklist](artifact/references/pre_flight_checklist.md)
- [Short-drama consistency](artifact/references/short_drama_consistency.md)
- [Short-drama genres](artifact/references/short_drama_genres.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown storyboard plans with structured prompt fields, shot lists, timelines, and optional HTML storyboard preview.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes engine/version labels, negative prompts, duration, timeline, camera, motion strength, multimodal reference advice, and quality gates.]

## Skill Version(s):

3.4.4 (source: server release metadata; artifact frontmatter reports 3.8.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
