## Description:

Turn user-provided meeting text into evidence-cited minutes and action items using the current model, validate the structured JSON against exact quotes, then save local Markdown and task CSV. Use for meeting minutes and follow-up lists; not audio transcription or calendar automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

People who need to turn provided meeting notes into evidence-cited minutes, decisions, action items, and open questions use this skill. It checks quoted source evidence and saves local Markdown minutes and a task CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting notes may contain confidential information processed by the configured model.

Mitigation: Confirm the model is allowed to handle the notes and protect saved transcript and report copies.

Risk: Matching quotations does not prove that extracted interpretations, responsibilities, or dates are correct.

Mitigation: Review summaries, responsibilities, and dates against the original meeting text.

Risk: Installing the CLI with @latest may change the version used between runs.

Mitigation: Use a reviewed CLI version for reproducible installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-meeting-actions)
- [MochiLab](https://mochilab.bz)
- [Extraction schema](artifact/references/extraction.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV]

**Output Format:** [Evidence-cited Markdown minutes, structured JSON, and task CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Items include source quotations and evidence IDs; unspecified owners and due dates remain unknown. Reports are saved locally.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
