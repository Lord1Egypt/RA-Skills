## Description:

Hash, HMAC, encode/decode, UUID generation, and hash identification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutthemustard](https://clawhub.ai/user/cutthemustard)

### License/Terms of Use:


## Use Case:

Developers and technical users use this skill to generate hashes and HMACs, encode or decode common formats, generate UUIDs, and identify possible hash algorithms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inputs are processed by a third-party API, so sensitive material could be exposed outside the user's local environment.

Mitigation: Do not send passwords, API keys, private keys, recovery phrases, proprietary data, or other secrets unless remote processing has been explicitly approved; use local tools for sensitive inputs.

## Reference(s):

- [Hash Generate on ClawHub](https://clawhub.ai/cutthemustard/skills/hash-generate)
- [Hash Agent Utility](https://hash.agentutil.net)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return hash values, HMACs, encoded or decoded strings, UUIDs, hash-identification results, request metadata, and service information.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
