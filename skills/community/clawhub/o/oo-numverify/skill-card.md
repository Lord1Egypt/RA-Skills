## Description:

Use this skill to look up supported countries and validate phone numbers with Numverify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to look up supported countries and their dialing codes, or to validate phone numbers and retrieve country, carrier, and line-type details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup can execute unverified remote code, and its broader effects have not been inspected.

Mitigation: Review the CLI installer and any skill synchronization effects before allowing automatic setup; prefer a reviewed, pinned installation and restrict unwanted skill synchronization.

Risk: Phone numbers submitted for validation are processed by OOMOL and Numverify.

Mitigation: Submit only phone numbers you intend OOMOL and Numverify to process.

## Reference(s):

- [Numverify API documentation](https://docs.apilayer.com/numverify/docs/numverify-api-v-1-0-0-2)
- [Numverify](https://numverify.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON connector results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include supported country dialing codes or phone validation details such as country, carrier, and line type.]

## Skill Version(s):

1.0.2 (source: artifact/SKILL.md frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
