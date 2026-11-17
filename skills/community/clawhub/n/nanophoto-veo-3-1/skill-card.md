## Description:

Generate Veo 3.1 videos through the NanoPhoto.AI API from text prompts, reference images, or first/last frames, with multi-shot workflows and status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanophotohq](https://clawhub.ai/user/nanophotohq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to submit and monitor NanoPhoto.AI Veo 3.1 video-generation jobs from text prompts, reference images, or first/last frames. It supports single-shot and multi-shot workflows with documented resolution, image, and polling rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, task IDs, and public image URLs are sent to a third-party NanoPhoto service during generation and status checks.

Mitigation: Submit only content the user is authorized to use, avoid private or sensitive media, and use public image URLs only when required by the selected generation mode.

Risk: The bundled script supports passing NANOPHOTO_API_KEY on the command line, which can expose secrets through shell history or process listings.

Mitigation: Configure NANOPHOTO_API_KEY through the platform's secure environment setting or environment variable instead of using the command-line API key option.

## Reference(s):

- [Veo 3.1 API Reference](references/api.md)
- [NanoPhoto.AI Homepage](https://nanophoto.ai)
- [ClawHub Skill Page](https://clawhub.ai/nanophotohq/skills/nanophoto-veo-3-1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON API payloads; raw JSON can be emitted by the bundled script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return task IDs, status responses, video URLs, timing details, and polling progress for submitted generation jobs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
