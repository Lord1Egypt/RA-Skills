## Description: <br>
Power Electronics helps agents solve AC-DC, DC-AC, DC-DC, and AC-AC power-electronics problems with topology selection, formulas, local calculation scripts, and Simulink guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanyinghao](https://clawhub.ai/user/shanyinghao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and power-electronics engineers use this skill to classify converter questions, calculate topology parameters and device stresses, cross-check formulas with local scripts, and prepare Simulink guidance for common AC-DC, DC-AC, DC-DC, and AC-AC designs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation keywords may cause the skill to engage on general power-electronics terms such as QR, rectification, or inversion. <br>
Mitigation: Confirm the user's converter type and requested task before applying formulas, scripts, or topology-specific guidance. <br>
Risk: Local calculation scripts can produce misleading engineering outputs when inputs or operating assumptions are wrong. <br>
Mitigation: Review script parameters and compare results against the documented formulas and expected operating mode before relying on them. <br>
Risk: The artifact includes optional publishing and token setup instructions that are only relevant to skill publishers. <br>
Mitigation: Follow publishing steps only when releasing the skill yourself, and keep any ClawHub or GitHub credentials out of shared logs and artifacts. <br>


## Reference(s): <br>
- [Four Power Conversions Overview](artifact/references/four-conversions.md) <br>
- [Power Electronics Formula Reference](artifact/references/formulas.md) <br>
- [Topology Selection Guide](artifact/references/topologies.md) <br>
- [Advanced Topics: PFC, Flyback, LLC, and Magnetics](artifact/references/advanced.md) <br>
- [Worked Examples](artifact/references/examples.md) <br>
- [Simulink and Simscape Templates](artifact/references/simulink-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON snippets and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include calculated converter values, topology notes, device-stress summaries, engineering cautions, and Simulink setup guidance.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
