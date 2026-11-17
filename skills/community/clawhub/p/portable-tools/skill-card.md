## Description:

Build cross-device tools without hardcoding paths or account names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tunaissacoding](https://clawhub.ai/user/tunaissacoding)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to design scripts and tools that work across devices by identifying variable paths, account names, configuration formats, and failure modes before implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OAuth and keychain debugging examples can lead users to expose tokens, keychain payloads, passwords, cookies, or raw credential records.

Mitigation: Use redacted values, boolean checks, expiration timestamps, or non-reversible fingerprints instead of pasting full secrets into chat, logs, screenshots, or tickets.

Risk: The checklist scans the directory supplied by the user and may inspect files outside the intended review scope if pointed too broadly.

Mitigation: Run the checklist only against directories intentionally selected for portability review.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a bash pre-publish checklist for scanning an intentionally selected target directory.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
