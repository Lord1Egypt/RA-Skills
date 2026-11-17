## Description:

Detects the language of text through the Detect Language service and supports related account and language lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to detect the language of one or more text inputs, check account status, or list supported languages through a connected Detect Language account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A language-detection request can trigger an unverified software installer without a separate approval step.

Mitigation: Review and approve the CLI installation separately before using the skill.

Risk: Bundled-skill synchronization may alter other agents.

Mitigation: Check whether synchronization is enabled and disable it if those changes are unwanted.

Risk: Text submitted for language detection is sent through OOMOL to Detect Language.

Mitigation: Submit only text you are authorized to send through OOMOL to Detect Language.

## Reference(s):

- [Detect Language](https://detectlanguage.com/)
- [Detect Language API documentation](https://detectlanguage.com/documentation/v3)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text and JSON, including language detection results and confidence scores]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account status or supported-language data.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
