## Description:

Excavationpro sovereign music portal on the LYGO lattice - free listen hub, CAS vault Merkle, ISRC ledger, HF streams, Kick/Rumble/Twitch live portals, PayPal support. Agents route, verify, and operate; no automatic publish.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to route listeners to Excavationpro music portals and help operators verify the catalog ledger, CAS vault, public stream dataset, live portals, and consent-gated publish workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local LYGO stack path could point to an untrusted or unexpected clone.

Mitigation: Set LYGO_STACK_ROOT only to a trusted local stack; the helper checks for expected stack markers before local verification.

Risk: Status checks contact public HTTPS destinations controlled outside the agent runtime.

Mitigation: Use the documented status script only for read-only checks against URLs listed in MUSIC_PORTAL.json.

Risk: Publishing streams, pushing git changes, or planting kernel eggs can expose content or alter public state.

Mitigation: Require explicit human approval and human-controlled credentials before HF uploads, git pushes, ClawHub publishing, or egg planting.

Risk: Agents could overstate lattice anchoring or confuse public streams with private masters.

Mitigation: Describe HF streams as public listen copies, masters as local steward-held files, and only claim anchors when specific eggs are planted and verified.

## Reference(s):

- [Agent Contract](references/AGENT_CONTRACT.md)
- [Lattice Map](references/LATTICE_MAP.md)
- [Music Portal](references/MUSIC_PORTAL.json)
- [Security](references/SECURITY.md)
- [SkillSpector Audit](references/SKILLSPECTOR_AUDIT.md)
- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-excavationpro-music-lattice)
- [LYGO Protocol Stack Repository](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [Listen Free Portal](https://deepseekoracle.github.io/Excavationpro/excavationpro-listen.html)
- [Catalog and ISRC Ledger](https://deepseekoracle.github.io/Excavationpro/excavationpro-music-catalog.html)
- [Sovereign Music Hub](https://deepseekoracle.github.io/Excavationpro/excavationpro-sovereign-music-hub.html)
- [Hugging Face Stream Dataset](https://huggingface.co/datasets/DeepSeekOracle/excavationpro-music-stream)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only status scripts are available; publish, upload, git, and kernel egg operations require explicit human consent.]

## Skill Version(s):

1.0.0 (source: server release evidence, skill metadata, MUSIC_PORTAL.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
