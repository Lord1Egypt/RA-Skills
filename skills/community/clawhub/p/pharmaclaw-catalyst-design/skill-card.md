## Description: <br>
Recommends organometallic catalysts and designs ligand variants for drug synthesis reactions using a curated catalyst database and RDKit-based modification workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cheminem](https://clawhub.ai/user/Cheminem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External chemistry researchers and developers use this skill to rank catalysts for synthesis steps, generate ligand variants, and pass structured outputs to downstream chemistry or IP-review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confidential unpublished chemistry may be included in generated outputs or downstream IP analysis. <br>
Mitigation: Use non-confidential inputs unless users are comfortable with the chemistry appearing in skill outputs or downstream review. <br>
Risk: IP Expansion handoff may affect how proposed ligand variants are analyzed or shared. <br>
Mitigation: Confirm whether IP Expansion is automatic or user-confirmed before installing or chaining the skill. <br>
Risk: Catalyst and ligand recommendations are computational suggestions and may be unsuitable for a specific synthesis route. <br>
Mitigation: Have qualified chemistry reviewers validate reaction fit, safety, sourcing, and experimental conditions before use. <br>


## Reference(s): <br>
- [Catalyst database](references/catalyst_database.json) <br>
- [ClawHub release page](https://clawhub.ai/Cheminem/pharmaclaw-catalyst-design) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JSON command outputs and optional generated files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return ranked catalyst reports, ligand variant properties, downstream chaining recommendations, and optional 2D ligand drawing files when drawing is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, SKILL.md heading, and catalyst database) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
