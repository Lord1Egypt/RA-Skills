## Description: <br>
Validate, normalize, export, and import openclaw.json configs with backups and schema checks before applying changes or upgrades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ether-btc](https://clawhub.ai/user/ether-btc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when editing OpenClaw configuration, validating candidate changes, normalizing fields, or moving configs between machines with config tokens and backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Config export may include literal API keys in a token that users expect to be safe to share. <br>
Mitigation: Do not share mrconf tokens from configs that may contain raw credentials; use ${REFERENCE} placeholders or patch export redaction before release. <br>
Risk: The validator path may run a mutating doctor --fix command outside the intended candidate file. <br>
Mitigation: Avoid the validator until doctor --fix is removed or fully isolated to the candidate file, and keep a verified backup of openclaw.json before validation. <br>
Risk: Imports and normalization can change live OpenClaw configuration and depend on sensitive credentials from environment variables or pass. <br>
Mitigation: Prefer interactive imports with visible diffs, validate before applying, and rely on automatic or manual backups for rollback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ether-btc/openclaw-config-safety) <br>
- [CONFIG-EDIT.md](references/CONFIG-EDIT.md) <br>
- [EXPORT-TOKEN-SPEC.md](references/EXPORT-TOKEN-SPEC.md) <br>
- [NORMALIZATION-SPEC.md](references/NORMALIZATION-SPEC.md) <br>
- [ONBOARDING-SPEC.md](references/ONBOARDING-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Text] <br>
**Output Format:** [Markdown with inline shell commands and configuration-token text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or consume mrconf:v1 tokens and may propose openclaw.json edits that require validation before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; SKILL.md frontmatter declares 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
