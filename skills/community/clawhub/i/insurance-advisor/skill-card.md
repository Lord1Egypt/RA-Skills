## Description:

Insurance Advisor provides insurance education, coverage comparisons, premium estimates, claim guidance, and term life or health insurance planning prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate insurance education, compare common policy categories, estimate premiums, and outline claim preparation steps. Outputs should be treated as general informational guidance, not licensed insurance, legal, medical, or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports a suspicious verdict because the package includes an insurance advisor, an under-disclosed finance logger, and a local command-execution input bug.

Mitigation: Review or fix the shell scripts before installation, and avoid passing untrusted text into term or calculation commands.

Risk: The bundled scripts can save finance or insurance notes locally in plaintext and export them from ~/.local/share/insurance-advisor.

Mitigation: Do not enter real ID numbers, bank details, diagnoses, policy numbers, full medical records, or other sensitive personal data.

Risk: Insurance, finance, health, and claim outputs may be incomplete or unsuitable for a user's jurisdiction or personal circumstances.

Mitigation: Treat outputs as general education and consult qualified professionals before buying coverage, making claims, or relying on estimates.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ckchzh/skills/insurance-advisor)
- [BytesAgain Homepage](https://bytesagain.com)
- [Insurance Advisor Tips](artifact/tips.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style text and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Chinese-language insurance guidance and local plaintext note/export behavior when bundled shell commands are used.]

## Skill Version(s):

2.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
