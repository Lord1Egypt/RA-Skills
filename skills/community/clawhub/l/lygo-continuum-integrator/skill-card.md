## Description:

LYGO Continuum Integrator is a local Python CLI skill that integrates text inputs into JSON receipts, phase-locks node identifiers, emits non-collapsing geodesic receipts, and verifies those receipt artifacts without network, shell, subprocess, credential, or publishing behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and agents use this skill to create and verify local JSON receipt artifacts from supplied text and node inputs. It is suited for workflows that need local-only receipt generation, phase-locking, and verification without network access or automatic publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can create parent directories and write JSON artifacts when a path is supplied with --write and --i-consent.

Mitigation: Review output paths before consenting to writes, prefer stdout receipts when possible, and only use --write with explicit human approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-continuum-integrator)
- [ClawHub release metadata link](https://clawhub.ai/deepseekoracle/lygo-continuum-integrator)
- [Homepage from metadata](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/clawhub/mirrors/lygo-continuum-integrator)
- [GitHub repository from metadata](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [Security reference](references/SECURITY.md)
- [SkillSpector audit reference](references/SKILLSPECTOR_AUDIT.md)
- [Quickstart](examples/quickstart.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with Python CLI commands and JSON receipt artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Receipt commands print JSON to stdout; file writes are opt-in and require both --write and --i-consent.]

## Skill Version(s):

1.0.1 (source: server release metadata, SKILL.md frontmatter, claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
