## Description:

Generates Chinese CEO-style daily briefings by collecting real-time technology, finance, AI, social, and open-source news from 28 sources, saving fetched data as JSON and synthesized reports as Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhlorra](https://clawhub.ai/user/yhlorra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to gather daily news from predefined web sources and produce Chinese executive briefings for leadership scanning, market awareness, and follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad web fetching and arbitrary URL fetching may access untrusted external pages or internal network services if run in a sensitive environment.

Mitigation: Run the skill only where broad web access is acceptable, block internal network ranges, and review requested URLs before execution.

Risk: Fetched article content and generated report context may be sent to external LLM providers such as MiniMax or OpenRouter.

Mitigation: Do not process confidential or regulated content with external LLM credentials, and configure provider keys only for approved accounts.

Risk: Credential access is under-disclosed and dependency versions are not pinned in the artifact.

Mitigation: Provide only narrowly scoped API keys, keep secrets out of reports, and install from pinned dependencies or a reviewed release.

## Reference(s):

- [Skill README](artifact/README.md)
- [General briefing instructions](artifact/references/briefing_general.md)
- [Finance briefing instructions](artifact/references/briefing_finance.md)
- [Technology briefing instructions](artifact/references/briefing_tech.md)
- [AI daily briefing instructions](artifact/references/briefing_ai_daily.md)
- [Social briefing instructions](artifact/references/briefing_social.md)
- [GitHub briefing instructions](artifact/references/briefing_github.md)
- [Integration briefing instructions](artifact/references/briefing_integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and JSON source data, with shell commands and configuration guidance for agents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default reports are Chinese-language and are saved under reports/YYYY-MM-DD when persistence is enabled.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
