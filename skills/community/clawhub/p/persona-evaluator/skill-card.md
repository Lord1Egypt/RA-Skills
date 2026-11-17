## Description:

Audits OpenPersona and peer LLM-agent personas through structural, semantic white-box, and semantic black-box modes, producing scored reports with strengths, issues, and actionable improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neiljo-gy](https://clawhub.ai/user/neiljo-gy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, persona authors, and agent reviewers use this skill to audit OpenPersona persona packs or remote LLM-agent personas for structural completeness, semantic quality, role fit, and actionable improvement paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to run OpenPersona CLI commands, including unpinned npx invocations.

Mitigation: Use a pinned local OpenPersona installation with a lockfile, especially in CI or environments that may contain secrets.

Risk: The skill includes remediation commands that can change persona files, such as refine --apply and update.

Mitigation: Require human review and approval before applying remediation commands or writing changes to persona content.

Risk: The skill may read persona content during structural or semantic white-box evaluation.

Mitigation: Run it only on persona content the user is authorized to inspect, and prefer black-box consent or passive-observation modes when filesystem access is unavailable.

## Reference(s):

- [ClawHub persona-evaluator listing](https://clawhub.ai/neiljo-gy/skills/persona-evaluator)
- [OpenPersona repository](https://github.com/acnlabs/OpenPersona)
- [persona-evaluator standalone repository](https://github.com/acnlabs/persona-evaluator)
- [OpenPersona persona-evaluator listing](https://openpersona.co/skill/persona-evaluator)
- [White-box Semantic Rubrics](references/RUBRICS.md)
- [Black-box Semantic Evaluation](references/BLACK-BOX.md)
- [Semantic Evaluation Report Formats](references/REPORT-FORMAT.md)
- [Changelog](CHANGELOG.md)
- [OpenPersona skill rubric review trail](https://github.com/acnlabs/OpenPersona/blob/main/docs/SKILL-RUBRIC.md)
- [OpenPersona skill rubric review trail session 2](https://github.com/acnlabs/OpenPersona/blob/main/docs/SKILL-RUBRIC-SESSION-2.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown reports, JSON evaluation output, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structural mode can emit JSON for scripting or CI; semantic white-box reports are intended to stay under about 500 words.]

## Skill Version(s):

0.3.4 (source: evidence.release.version, frontmatter metadata.version, changelog released 2026-04-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
