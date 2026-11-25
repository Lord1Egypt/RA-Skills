## Description:

Собирает ежедневный дайджест топ-5 новостей (ИИ, робототехника, финтех) из Telegram-каналов и Google News, отбирает их LLM-агентами, переводит статьи на русский и сохраняет переводы в PDF в папки агента.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dariaakimov](https://clawhub.ai/user/dariaakimov)

### License/Terms of Use:

MIT-0

## Use Case:

Пользователи запускают навык, чтобы собрать дайджест из пяти свежих новостей об ИИ, робототехнике и финтехе, получить русские переводы статей в PDF и сохранить сводку с файлами результатов.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a browser redirect risk that could send requests to private network services.

Mitigation: Review the reported redirect risk and install only in an environment where access to sensitive internal services is acceptable.

Risk: Dependencies are unpinned and the scan is partial because some local references could not be resolved.

Mitigation: Review dependency versions and resolve the missing scan references before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dariaakimov/skills/newsbot-digest)

## Skill Output:

**Output Type(s):** [Markdown, HTML, JSON, PDF, Spreadsheet files]

**Output Format:** [Russian-language news digest with translated article PDFs and supporting HTML, JSON, and XLSX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selects up to five stories per run; includes local paths or links to generated translation PDFs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
