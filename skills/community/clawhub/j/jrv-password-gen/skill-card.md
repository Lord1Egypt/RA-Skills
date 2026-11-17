## Description:

Generate secure passwords, passphrases, and PINs with entropy analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate random passwords, passphrases, and PINs, or to check password strength with entropy estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passphrase mode may make an outbound request and cache a shared word list, which could weaken generated passphrases.

Mitigation: Review before installing, prefer a version that bundles or verifies its word list, and avoid passphrase mode where outbound retrieval or shared cache reuse is unacceptable.

Risk: Using the documented --analyze argument form with real passwords can expose sensitive passwords through command history or process arguments.

Mitigation: Avoid analyzing real passwords with command-line arguments; use a version that prompts securely or analyze only test values.

## Reference(s):

- [EFF Large Wordlist](https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON, with shell command examples when guiding use]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated secrets, passphrases, PINs, and entropy or strength analysis]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
