## Description: <br>
Multi Model Consensus coordinates multiple selected models to independently review, debate, score, and synthesize decision guidance into a consensus report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zeekr0808-hue](https://clawhub.ai/user/zeekr0808-hue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to route complex decisions through a configurable committee of models, compare scores, surface disagreements, and receive a structured consensus recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may share submitted decision materials with several selected model providers. <br>
Mitigation: Use only providers acceptable for the material being reviewed, and avoid confidential, regulated, or proprietary content unless those providers are approved. <br>
Risk: Final reports may be archived in OpenClaw memory or written to the Desktop. <br>
Mitigation: Review output locations and remove or relocate sensitive reports according to local data-handling policy. <br>
Risk: Consensus reports can still contain incorrect or misleading recommendations. <br>
Mitigation: Treat the report as decision support and have a responsible user review the rationale, scores, and risk notes before acting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zeekr0808-hue/multi-model-consensus) <br>
- [User Guide](docs/USER_GUIDE.md) <br>
- [Output Template](references/OUTPUT_TEMPLATE.md) <br>
- [State Machine Reference](references/STATE_MACHINE.md) <br>
- [Troubleshooting Guide](references/TROUBLESHOOTING.md) <br>
- [Verification Case](references/VERIFICATION_CASE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown consensus reports with scoring matrices, decision-point status, rationale summaries, and risk notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports configurable model committee size, review rounds, thresholds, and pass criteria; reports may be archived locally or written to Desktop.] <br>

## Skill Version(s): <br>
1.9.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
