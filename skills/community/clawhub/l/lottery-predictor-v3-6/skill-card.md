## Description:

Generates entertainment-oriented Shuangseqiu lottery recommendations from local historical data, returning ranked red and blue balls, candidate combinations, and verification summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mumuli2021](https://clawhub.ai/user/mumuli2021)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users use this skill for entertainment-oriented Shuangseqiu lottery analysis, including ranked number pools, candidate combinations, and post-draw verification. It should not be treated as financial advice or a reliable way to win random lottery games.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may over-rely on unsupported lottery performance claims or treat predictions as financial guidance.

Mitigation: Present outputs as entertainment only, retain the gambling disclaimer, and require independent validation for any hit-rate claims.

Risk: The package contains mismatched V3.6 and V2.15 assets, and package metadata dispatches prediction to the older script.

Mitigation: Review and reconcile the active entry points before deployment so users know which model version is actually running.

Risk: The bundled publishing script could use an operator's ClawHub account if run.

Mitigation: Do not run auto_publish.sh during normal skill use; remove or isolate publishing utilities before distributing or installing the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mumuli2021/skills/lottery-predictor-v3-6)
- [Publisher profile](https://clawhub.ai/user/mumuli2021)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact package metadata](artifact/package.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON-style text containing ranked lottery numbers, scored recommendations, candidate combinations, and verification summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.8+, SQLite3, and a local LOTTERY_DB_PATH database; package metadata declares no network permission.]

## Skill Version(s):

3.6.0 (source: evidence.json release.version, target metadata, and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
