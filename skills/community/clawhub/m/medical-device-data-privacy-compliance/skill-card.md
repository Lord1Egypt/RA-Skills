## Description:

Data-compliance companion for medical devices sold across borders: it maps how patient and device data flows through apps, cloud backends and service partners, then checks each flow against GDPR, HIPAA, China's PIPL and cross-border transfer rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Medical-device manufacturers and privacy or compliance teams use this skill to map patient and device data flows across markets, identify privacy and cross-border transfer questions, and prepare DPIA/PIA notes and launch checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Descriptions containing identifiable patient information could expose sensitive data.

Mitigation: Use redacted descriptions and do not include identifiable patient records.

Risk: Generated compliance documents may reflect outdated requirements or be mistaken for professional legal advice.

Mitigation: Have a qualified professional check current requirements before relying on the documents.

Risk: The bundled file hash record does not match SKILL.md, which can affect confidence in package integrity.

Mitigation: Request an updated manifest if provenance or package integrity matters.

## Reference(s):

- [GDPR and Medical Devices](artifact/references/01-GDPR与医疗器械.md)
- [HIPAA and Medical Devices](artifact/references/02-HIPAA与医疗器械.md)
- [PIPL and Cross-border Data Assessment](artifact/references/03-个保法与数据出境评估.md)
- [Medical Device Data-flow Mapping Template](artifact/references/04-出海器械数据流映射模板.md)
- [LGD theory (linked in the skill materials)](https://github.com/zhaoxinghua09-cell/LGD)
- [Formal paper (linked in the skill materials)](https://doi.org/10.5281/zenodo.22456647)
- [Publisher-listed skill page](https://clawhub.ai/zhaoxinghua09-cell/skills/medical-device-data-privacy-compliance)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown checklists, data-flow tables, and privacy assessment notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include data-flow inventories, PIA/DPIA notes, cross-border compliance actions, and privacy-policy draft points.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
