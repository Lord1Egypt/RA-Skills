## Description:

Assist in drafting professional peer review response letters for academic journal and conference submissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT

## Use Case:

Researchers, authors, and academic teams use this skill to turn reviewer comments and revision notes into structured point-by-point response letters with an appropriate scholarly tone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer and local script introduce filesystem and package-install risk beyond the drafting task.

Mitigation: Review before installing, use a constrained workspace, and remove or lock unnecessary dependencies before running.

Risk: Writable output paths can overwrite existing files.

Mitigation: Choose output paths deliberately and inspect target files before running the script.

Risk: Drafted responses may contain inaccurate manuscript changes, locations, or technical claims.

Mitigation: Have the author or research team verify every response against the revised manuscript before submission.

## Reference(s):

- [Response Templates for Peer Review Letters](references/response_templates.md)
- [Academic Tone Guidelines](references/tone_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/peer-review-response-drafter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown, plain text, or LaTeX response letter]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include salutation, reviewer-by-reviewer numbered responses, manuscript-location references, and closing text.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
