## Description:

Generate narrative budget justifications for NIH/NSF applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External grant writers, researchers, and research administrators use this skill to draft narrative justifications for personnel, equipment, supplies, and travel budget categories in NIH or NSF proposals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes output files locally, so an incorrect output path could overwrite or disclose local proposal material.

Mitigation: Choose output paths deliberately and review generated files before sharing them.

Risk: The bundled script is draft-quality and does not implement the documented JSON/CSV input workflow.

Mitigation: Treat the current script as limited demo functionality unless the missing input handling is added and tested.

Risk: Generated budget narratives may be incomplete or unsuitable for a specific funding opportunity.

Mitigation: Have a knowledgeable reviewer verify agency requirements, budget details, and proposal claims before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/grant-budget-justification)
- [Publisher profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Plain text narrative budget justification; markdown output is documented, but the bundled script currently writes plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script can print a demo justification and write a local output file.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
