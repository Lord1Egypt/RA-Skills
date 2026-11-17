## Description:

Reviews the permissions required by a skill, script, or workflow and suggests least-privilege alternatives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and skill maintainers use this skill to turn permission requirements and runtime context into a review draft covering the current footprint, over-permissioning, least-privilege alternatives, isolation guidance, and a review checklist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process permission reviews that include sensitive operational details.

Mitigation: Use explicit, non-sensitive or redacted inputs where possible, following the evidence guidance.

Risk: The artifact includes broader inactive audit helpers in the local script that may not be obvious from the primary structured-brief mode.

Mitigation: Document or remove inactive helper paths before deployment if they are not intended for supported use.

Risk: Documentation and generated report labels are primarily Chinese-language, which can limit review by non-Chinese-speaking teams.

Mitigation: Have an appropriate reviewer check the generated Markdown or provide localized templates before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/permission-footprint-reviewer)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)
- [Artifact README](artifact/README.md)
- [Skill specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Structured Markdown, with optional JSON wrapper from the local Python script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces review drafts and checklists from local input; the script can write output to a user-selected file.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
