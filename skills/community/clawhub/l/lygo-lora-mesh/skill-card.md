## Description:

LYGO LoRa mesh encodes, decodes, probes, and compares compact Layer D roots_digest pulses for stock Meshtastic LoRa text messages without driving radios, networking, subprocesses, or firmware flashing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and engineers use this skill to generate and inspect compact LY1 roots_digest pulses for Meshtastic-based LoRa fallback workflows, including local encode/decode, probe, and comparison steps. It is aimed at off-grid mesh/status signaling rather than firmware flashing or radio control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command can use the latest ClawHub CLI package rather than a pinned CLI version.

Mitigation: Pin or otherwise verify the ClawHub CLI before installation when release reproducibility or supply-chain review is required.

Risk: A separate stack ingest command can write the documented lora_last.json state file when run intentionally.

Mitigation: Run stack ingest only with explicit consent and only in a checkout where writing data/living_mesh/lora_last.json is expected.

## Reference(s):

- [Hardware - stock Meshtastic only](references/HARDWARE.md)
- [Security - lygo-lora-mesh v1.0.0](references/SECURITY.md)
- [SkillSpector audit](references/SKILLSPECTOR_AUDIT.md)
- [Meshtastic documentation](https://meshtastic.org/docs/)
- [LYGO LoRa mesh on ClawHub](https://clawhub.ai/deepseekoracle/skills/lygo-lora-mesh)
- [LYGO living mesh on ClawHub](https://clawhub.ai/deepseekoracle/skills/lygo-living-mesh)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local stdout-oriented workflows; optional filesystem reads for badge or pulse files; no writes in packaged scripts.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, claw.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
