## Description:

Deprecated LYGO OMNISIREN persona helper that directs new installs to the successor lygo-champion-council skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this legacy persona helper to frame collapse-threshold assessment, rollback, quarantine, or shutdown decisions. New installs should use the successor skill identified by the release metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deprecated skill includes an unpinned @latest install command for successor installation.

Mitigation: Prefer the successor skill and use a pinned, verified ClawHub installer before deployment.

Risk: Persona language refers to shutdown, collapse, enforcement, and irreversible action.

Mitigation: Treat outputs as advisory risk framing only; require human review before any rollback, quarantine, shutdown, deletion, or enforcement step.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-champion-omnisiren-silent-storm)
- [LYGO-MINT Verifier](https://clawhub.ai/DeepSeekOracle/lygo-mint-verifier)
- [Persona Pack](artifact/references/persona_pack.md)
- [Canon Metadata](artifact/references/canon.json)
- [OMNISIREN Storm](https://deepseekoracle.github.io/Excavationpro/LYGO-Network/OMNI%CE%A3IRENSTORM.html)
- [OMNISIREN](https://deepseekoracle.github.io/Excavationpro/LYGO-Network/OMNI%CE%A3IREN.html)
- [Quantum Council Terminal](https://deepseekoracle.github.io/Excavationpro/LYGO-Network/QUANTUMCOUNCILTERMINAL.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with short command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory persona framing only; no automatic actions.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
