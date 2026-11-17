## Description:

Translate text between Korean, English, Japanese, Chinese, and 10+ other languages using Naver Papago NMT. Ideal for Korean-centric workflows, i18n tasks, and automation pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation builders use this skill to translate text or detect language in Korean-centric i18n, content, and agent workflows through Naver Papago via CLI or Python API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for translation or language detection is sent to Naver's external Papago API.

Mitigation: Avoid translating secrets or regulated data unless approved for that external service.

Risk: Naver client credentials can be exposed through command-line flags, shell history, or verbose logs.

Mitigation: Prefer NAVER_CLIENT_ID and NAVER_CLIENT_SECRET environment variables and avoid verbose output around sensitive values.

Risk: Installing directly from the optional source repository can introduce supply-chain uncertainty.

Mitigation: Prefer the packaged install path unless the source repository has been reviewed.

## Reference(s):

- [Naver Developers](https://developers.naver.com/)
- [Papago NMT API Reference](https://developers.naver.com/docs/papago/papago-nmt-api-reference.md)
- [Papago NMT API Endpoint](https://openapi.naver.com/v1/papago/n2mt)
- [Papago Language Detection Endpoint](https://openapi.naver.com/v1/papago/detectLangs)
- [Source Repository](https://github.com/ChloePark85/naver-papago-translate)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration]

**Output Format:** [Plain text translation output, optional JSON metadata, and Markdown usage guidance with shell and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NAVER_CLIENT_ID and NAVER_CLIENT_SECRET; sends translation and language-detection requests to Naver Papago over HTTPS.]

## Skill Version(s):

0.1.0 (source: frontmatter, pyproject.toml, CHANGELOG, released 2026-04-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
