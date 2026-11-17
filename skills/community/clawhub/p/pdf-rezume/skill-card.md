## Description:

Создаёт одностраничное русскоязычное резюме PDF-отчёта для руководителя с ключевыми выводами и вопросами для обсуждения.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iirtegova](https://clawhub.ai/user/iirtegova)

### License/Terms of Use:

MIT-0

## Use Case:

Руководители и их команды используют навык, чтобы получить краткое резюме PDF-отчёта с проверенными по документу числами и вопросами для обсуждения.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local job state retains a copy of the PDF, extracted text and generated outputs that may contain sensitive information.

Mitigation: Use only documents approved for local processing; protect the job state and remove it according to your retention policy.

Risk: OCR or chart interpretation can omit text or associate figures with the wrong context despite numeric checks.

Mitigation: Review the source pages and cited figures before relying on or sharing the summary.

## Reference(s):

- [ClawHub: pdf-rezume](https://clawhub.ai/iirtegova/skills/pdf-rezume)
- [Канон одностраничного резюме для руководителя](artifact/references/summary_canon.md)

## Skill Output:

**Output Type(s):** [PDF file, JSON status, Optional HTML file]

**Output Format:** [One-page A4 PDF; JSON progress and validation responses; HTML copy on request]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Russian-language summary; supports text-based Russian and English PDFs and offline OCR for Latin-script scans. Cyrillic scans require an additional OCR model.]

## Skill Version(s):

1.3.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
