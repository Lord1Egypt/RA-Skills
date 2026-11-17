## Description:

LYGO Continuum creates falsifiable work capsules for AI agents and humans, sealing done-claims as checkable file hashes, content checks, JSON paths, and confined globs that can be re-verified for drift and handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers, external agent operators, and reviewers use this skill to seal completed work as local claims, verify capsules later, detect drift, and prepare portable handoffs for another human or AI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted capsules can steer local file reads during verification.

Mitigation: Review capsule contents before use and always pass an explicit --base for the intended project.

Risk: Generated handoff or witness-card outputs can contain active or agent-directed content from capsule data.

Mitigation: Inspect generated outputs from untrusted capsules before following instructions, sharing them, or opening generated HTML.

Risk: The optional browser portal is separate from the local CLI and requires trusting an external site with pasted or dropped files.

Mitigation: Use the portal only for non-sensitive files and treat it separately from the skill's no-network CLI behavior.

Risk: Installing with a floating latest installer can pull a different package than expected.

Mitigation: Prefer a pinned installer or otherwise verify the release version and source before installation.

## Reference(s):

- [LYGO Continuum ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-continuum)
- [LYGO Continuum homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-continuum)
- [Security notes](references/SECURITY.md)
- [SkillSpector audit response](references/SKILLSPECTOR_AUDIT.md)
- [ClawHub security audit](https://clawhub.ai/deepseekoracle/skills/lygo-continuum/security-audit)
- [Quickstart](examples/quickstart.md)
- [Optional browser portal](https://chatagent.ca/lygo-continuum.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI status text, JSON capsules, Markdown handoff packs, and optional HTML witness cards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local files or terminal text; capsule verification can return nonzero exit codes when claims fail, drift is detected, or root integrity fails.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, claw.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
