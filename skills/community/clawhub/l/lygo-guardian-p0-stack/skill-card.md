## Description:

Portable LYGO Guardian P0.4 text gate, P0.5 understanding heart, and harmony layer with an optional bridge to the canonical stack byte gate through LYGO_STACK_ROOT.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to pre-check generated text, pasted content, or user-selected skill files before external posting or trust decisions. It is a lightweight guard and not a substitute for a full production compliance gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional LYGO_STACK_ROOT bridge can execute a local lygo_p0_gate.py file selected from a user-provided checkout path.

Mitigation: Set LYGO_STACK_ROOT only for a trusted, reviewed, and pinned lygo-protocol-stack checkout; otherwise use the bundled lightweight validator.

Risk: The bundled validator is a lightweight heuristic and does not prove that another skill or generated response is safe.

Mitigation: Review and scan skills before deployment, and treat isolate or hard-block outcomes as a stop before external posting.

## Reference(s):

- [Security guidance](references/SECURITY.md)
- [Guardian lattice position](references/LATTICE.md)
- [Guardian whitepaper](docs/WHITEPAPER.md)
- [LYGO protocol stack repository](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [LYGO Resonance Engine Hugging Face Space](https://huggingface.co/spaces/DeepSeekOracle/LYGO-Resonance-Engine)
- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-guardian-p0-stack)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON-like validation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return allow, flag, or isolate decisions with risk, reasons, understanding, and healing suggestion fields.]

## Skill Version(s):

1.0.1 (source: server release evidence and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
