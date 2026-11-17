## Description:

Provides a practical playbook for comparing medical-device post-market surveillance duties across the US, EU, China, and Japan, with adverse-event, PSUR, FSCA/recall, PMCF, and planning checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Regulatory, quality, and clinical teams use the skill to compare post-market obligations across four markets, review adverse-event reporting workflows, and draft PMS/PSUR plans and FSCA or recall checklists.

### Deployment Geography for Use:

Global (guidance covers the US, EU, China, and Japan)

## Known Risks and Mitigations:

Risk: The toolkit's stated 90-day US serious-injury reporting deadline conflicts with the general 30-calendar-day manufacturer requirement cited in the security guidance.

Mitigation: Verify event classification and reporting deadlines against current FDA requirements before acting.

Risk: The bundled audit cites unrelated script names, and the attestation contains a stale SKILL.md checksum.

Mitigation: Do not treat those files as independent assurance; verify the release contents and checksums against a trusted source.

## Reference(s):

- [Post-market surveillance knowledge base](references/上市后监管知识库.md)
- [FDA Mandatory Reporting Requirements for Manufacturers](https://www.fda.gov/medical-devices/postmarket-requirements-devices/mandatory-reporting-requirements-manufacturers-importers-and-device-user-facilities)
- [21 CFR Part 803: Medical Device Reporting](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-803)
- [MDCG 2022-21: Periodic Safety Update Report guidance](https://health.ec.europa.eu/document/download/a7df24c3-d4a3-4218-a8e0-726febfa01c2_en?filename=mdcg_2022-21_en.pdf)
- [China medical device adverse-event monitoring measures](https://www.samr.gov.cn/cms_files/filemanager/samr/www/samrnew/samrgkml/nsjg/bgt/202106/W020211127427208653527.pdf)
- [PMDA medical device adverse-event reporting](https://www.pmda.go.jp/safety/reports/mah/0006.html)
- [LGD ecosystem hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Shell commands]

**Output Format:** [Text and Markdown checklists or planning frameworks, with optional local command-line results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May be tailored by market and device class; the bundled toolkit operates locally without external services.]

## Skill Version(s):

1.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
