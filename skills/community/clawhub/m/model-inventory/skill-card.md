## Description:

Scans installed AI coding CLIs, verifies active model access through explicit probes, and writes a cached model inventory with role-to-model routing recommendations for downstream agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisrongo](https://clawhub.ai/user/dennisrongo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inventory local AI coding CLIs, confirm which accounts and models are usable, and publish a fresh routing cache for other agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maps local AI CLIs, credential-presence signals, configured or default models, and verified model access, which can reveal sensitive account and tooling metadata.

Mitigation: Install only when that local inventory is acceptable to collect, use quick scan for local-only detection when probes are not desired, and treat ~/.claude/model-inventory.json as sensitive.

Risk: Credential presence alone can be mistaken for active account or model entitlement.

Mitigation: Use the documented evidence tiers and rely on live probe results before marking models verified or routing agents to them.

## Reference(s):

- [CLI Registry](references/cli-registry.md)
- [ClawHub model-inventory release](https://clawhub.ai/dennisrongo/skills/model-inventory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report plus JSON inventory file and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes ~/.claude/model-inventory.json and reports observed CLI/model status, probe evidence, routing choices, and probe cost.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
