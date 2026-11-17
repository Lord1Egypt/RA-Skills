## Description:

Breaks the independent claims of two or three patents into technical features and compares similarities and differences in a feature comparison table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Patent professionals and researchers can compare the technical features in two or three patents' claims and prepare a structured comparison table. The comparison is textual guidance, not a legal determination of infringement, equivalence, or inventiveness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API credentials may be sent to an unintended server.

Mitigation: Prefer the free trial until credential handling is fixed; avoid pasting paid keys into chat, restrict access to saved keys, and verify the credential destination before use.

Risk: Search terms may disclose confidential information, and paid API use can incur charges.

Mitigation: Approve confidential disclosures before sending search terms to PatentMax and agree on spending limits before paid use.

## Reference(s):

- [Patent Claim Compare on ClawHub](https://clawhub.ai/ip930/skills/patent-claim-compare)
- [PatentMax service](https://api.ip930.com)
- [API reference](artifact/references/api-reference.md)
- [Query syntax](artifact/references/query-syntax.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, CSV]

**Output Format:** [Chinese-language findings and a UTF-8 CSV feature comparison table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compares two or three patents; defaults to independent claims and does not provide legal conclusions.]

## Skill Version(s):

1.0.2 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
