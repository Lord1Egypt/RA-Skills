## Description:

LYGO Flame Ward helps agents locally scan operator-supplied text, skill directories, and HTML/JS snippets for disinformation patterns, authority-only claims, digest mismatches, and silent WebAudio fingerprinting, then gate, quarantine, or produce audit receipts with consent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers, operators, and agent workflows use this skill to review local content or skill artifacts before treating them as trusted inputs. It is suited for local ingest gating, heuristic claim review, endpoint snippet checks, and consent-gated quarantine or receipt generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local heuristics may label or gate incomplete but legitimate content as unverified or risky.

Mitigation: Use the skill as a review aid, inspect the generated reasons and classes, and avoid treating its verdict as a final truth determination.

Risk: Outputs could be misused as medical, legal, identity, or final authority judgments.

Mitigation: Keep the skill scoped to local content review and require qualified human review for medical, legal, identity, or other high-impact decisions.

Risk: Operator-supplied files or skill directories may contain sensitive local data.

Mitigation: Pass only files and directories intended for inspection and review generated JSON before sharing it outside the local environment.

Risk: Quarantine and burn-receipt commands can create local JSON artifacts.

Mitigation: Use --i-consent only when local writes are intended and choose output paths deliberately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-flame-ward)
- [ClawHub release metadata link](https://clawhub.ai/deepseekoracle/lygo-flame-ward)
- [OpenClaw homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/clawhub/mirrors/lygo-flame-ward)
- [Security notes](references/SECURITY.md)
- [SkillSpector audit notes](references/SKILLSPECTOR_AUDIT.md)
- [Quickstart](examples/quickstart.md)
- [Enemy model](data/ENEMY_MODEL.json)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON objects and concise text from local CLI commands, with process exit codes for ingest gating]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-only output; quarantine and burn-receipt JSON files are written only when --i-consent is provided.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, claw.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
