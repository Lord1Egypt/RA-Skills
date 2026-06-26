## Description: <br>
Audits existing mobile UI for field low-visibility conditions such as low light, glare, gloves, wet hands, and vibration, then emits a structured handoff document set with findings and prioritized fix recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentjiang06](https://clawhub.ai/user/vincentjiang06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, frontend engineers, field app maintainers, and implementer agents use this skill to audit existing H5, app, or WeChat mini-program UI for field readability and tap reliability. It produces audit reports and fix-plan guidance for another implementer to apply. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runtime themes, background images, and JavaScript-driven states may require visual judgment rather than exact static measurements. <br>
Mitigation: Use the bounded visual/browser pass, label estimates clearly, and rerun with the relevant CSS or a narrower page/component scope when exact evidence is needed. <br>
Risk: Fix recommendations can be misapplied if treated as automatic edits. <br>
Mitigation: Keep the skill in audit-only mode, review the generated audit.json and report.md, and have an implementer apply changes in a separate step. <br>
Risk: Audit output files may include details from local UI source files. <br>
Mitigation: Run on the intended scoped target only and review generated reports before sharing outside the project. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vincentjiang06/low-visibility-fix) <br>
- [Design tokens](artifact/references/design-tokens.json) <br>
- [Field conditions](artifact/references/field-conditions.md) <br>
- [Research bibliography](artifact/references/research-bibliography.md) <br>
- [Audit protocol](artifact/rules/audit-protocol.md) <br>
- [Handoff document contract](artifact/rules/handoff-docs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown report and JSON audit sidecar, with concise terminal summaries and scoped rerun commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes audit.json and report.md to the configured output directory; target source files are not edited.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact changelog lists 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
