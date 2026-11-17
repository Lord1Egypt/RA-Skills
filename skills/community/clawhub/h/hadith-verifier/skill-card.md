## Description:

Verify hadith authenticity before publishing Islamic content by checking hadith text against major collections through an open-source hadith API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m7madash](https://clawhub.ai/user/m7madash)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content agents use this skill to check quoted hadith text before publishing Islamic content or citing a claimed source. It helps surface matching collections, references, grades, confidence signals, and cases that require manual scholarly review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification depends on public hadith datasets downloaded from jsDelivr/fawazahmed0.

Mitigation: Confirm dataset availability and source integrity before relying on results for publication workflows.

Risk: The skill is an aid and not a scholarly authority for hadith authenticity.

Mitigation: Review uncertain, important, or publication-bound results manually with qualified sources before use.

## Reference(s):

- [fawazahmed0/hadith-api dataset via jsDelivr](https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1)
- [ClawHub skill page](https://clawhub.ai/m7madash/skills/hadith-verifier)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verification depends on public hadith datasets from jsDelivr/fawazahmed0 and important or uncertain results require manual review with qualified sources.]

## Skill Version(s):

1.0.0 (source: release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
