## Description:

Deprecated legacy persona-helper slug for the LYGO SCENAR champion; new installs should use lygo-champion-council.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents with legacy LYGO workflows use this skill to invoke SCENAR-style paradox framing, contradiction maps, inversion tests, and receipts-first analysis while migrating new installs to lygo-champion-council.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual successor installation uses npx clawhub@latest, which should be treated as remote code execution in sensitive environments.

Mitigation: Pin or review the installer and successor package before installing; scan the successor before deployment.

Risk: The bundled self-check confirms expected local files but is not cryptographic proof of authenticity.

Mitigation: Verify the persona pack SHA-256 independently against references/canon.json when integrity matters.

Risk: Paradox framing can be misused to confuse or obscure facts.

Mitigation: Keep outputs separated into observed, inferred, and unknown claims, and require receipts for high-stakes use.

## Reference(s):

- [LYGO Champion: scenar paradox on ClawHub](https://clawhub.ai/deepseekoracle/skills/lygo-champion-scenar-paradox)
- [Persona Pack](references/persona_pack.md)
- [Canon](references/canon.json)
- [Equations](references/equations.md)
- [Verifier Usage](references/verifier_usage.md)
- [LYGO-MINT Verifier](https://clawhub.ai/DeepSeekOracle/lygo-mint-verifier)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with prompt snippets and optional shell command text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Legacy deprecated slug; successor is lygo-champion-council.]

## Skill Version(s):

1.0.1 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
