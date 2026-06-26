## Description: <br>
Objective, source-traceable evaluation of HiFi gear across transducers and source gear, producing bilingual evidence-traced verdicts for objective sound assessment and A/B comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentjiang06](https://clawhub.ai/user/vincentjiang06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to evaluate HiFi transducers and source gear from public measurements, review consensus, and documented priors. It is intended for objective sound assessment, source-gear competence checks, and evidence-grounded A/B comparison, not buying advice, EQ tuning, speakers, or non-audio tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate automatically for HiFi-related prompts and tends to answer bilingually with Chinese first. <br>
Mitigation: Use an explicit invocation or ask for single-language output when that behavior is not desired. <br>
Risk: Audio conclusions can become misleading when measurements, rigs, targets, or review sources are missing or incompatible. <br>
Mitigation: Require source provenance, rig and target compatibility checks, explicit gaps, dissent reporting, and the bundled validation gate before accepting outputs. <br>
Risk: Using the skill outside its stated scope can produce unsuitable guidance. <br>
Mitigation: Restrict use to objective HiFi transducer and source-gear evaluation or comparison; reject buying recommendations, EQ tuning, speakers, and non-audio tasks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vincentjiang06/skills/hifi-review) <br>
- [Research Bibliography](artifact/references/research-bibliography.md) <br>
- [Source Registry](artifact/references/source-registry.json) <br>
- [Targets](artifact/references/targets.json) <br>
- [Band Taxonomy](artifact/references/band-taxonomy.json) <br>
- [Source Gear Thresholds](artifact/references/source-gear-thresholds.json) <br>
- [Signature Glossary](artifact/references/signature-glossary.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Bilingual Markdown reviews with traceable JSON analysis outputs and inline shell command checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Claims are tagged as measured, consensus, or prior; long-form mode targets about 4000 CJK characters when evidence supports it.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact changelog top entry is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
