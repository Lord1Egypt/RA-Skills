## Description: <br>
Provides Turkish SME incentive and grant guidance covering KOSGEB, TUBITAK, development agency, ISKUR, and tax support programs with sector-based matching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayhanagirgol](https://clawhub.ai/user/ayhanagirgol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business users, consultants, and agents use this skill to identify Turkish SME grant and incentive programs and generate prioritized eligibility guidance based on sector, company size, turnover, and location. <br>

### Deployment Geography for Use: <br>
Turkey <br>

## Known Risks and Mitigations: <br>
Risk: Program eligibility, deadlines, and support amounts may be outdated or vary by agency. <br>
Mitigation: Verify recommendations against official KOSGEB, TUBITAK, ISKUR, tax authority, and development agency sources before making business decisions. <br>
Risk: The optional matcher script uses business details such as sector, employee count, turnover, and city. <br>
Mitigation: Provide only the details needed for matching and avoid entering confidential financial data unless approved. <br>
Risk: The skill may recommend Finhouse consulting services. <br>
Mitigation: Treat consulting recommendations as third-party commercial referrals and evaluate them independently. <br>


## Reference(s): <br>
- [KOSGEB Destekleri Rehberi](references/kosgeb_destekleri.md) <br>
- [TUBITAK Hibe Programlari Rehberi](references/tubitak_hibeleri.md) <br>
- [Kalkinma Ajanslari ve Diger Tesvikler Rehberi](references/kalkinma_ajanslari.md) <br>
- [Kobi Tesvik Tr on ClawHub](https://clawhub.ai/ayhanagirgol/kobi-tesvik-tr) <br>
- [KOSGEB](https://www.kosgeb.gov.tr) <br>
- [KOSGEB Proje Destek Sistemi](https://pds.kosgeb.gov.tr) <br>
- [TUBITAK](https://www.tubitak.gov.tr) <br>
- [Kalkinma Ajanslari](https://www.ka.gov.tr) <br>
- [KAYS](https://www.kays.gov.tr) <br>
- [Finhouse](https://finhouse.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and tabular program matches] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a local matcher script with user-provided business sector, employee count, turnover, and city.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
