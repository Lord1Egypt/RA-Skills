## Description:

Automates academic literature search, recommendation, multi-channel paper download attempts, Ablesci help-request monitoring, notifications, and progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oreosofat](https://clawhub.ai/user/oreosofat)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and knowledge workers use this skill to find academic papers, review ranked literature results, attempt lawful open-access downloads, and track requested paper downloads through completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests powerful browser, posting, file-write, subprocess, and recurring cron authority.

Mitigation: Review before installing, require confirmation for each Ablesci post and cron task, and keep download and progress paths scoped to a non-sensitive folder.

Risk: Browser automation through CDP can expose an active browsing session if configured broadly.

Mitigation: Use a dedicated temporary browser profile and avoid wildcard CDP origins.

Risk: The workflow depends on other skills and external services for search, browser control, and cron monitoring.

Mitigation: Pin or verify dependency skills before use and confirm service-specific actions before they run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oreosofat/skills/literature-research-pipeline)
- [Unpaywall API endpoint referenced by the skill](https://api.unpaywall.org/v2/{DOI}?email={LIT_UNPAYWALL_EMAIL})
- [DOI resolver endpoint referenced by the skill](https://doi.org/{DOI})
- [Semantic Scholar PDF endpoint referenced by the skill](https://api.semanticscholar.org/graph/v1/paper/{DOI}/PDF)
- [Crossref works endpoint referenced by the skill](https://api.crossref.org/works/{DOI})
- [Ablesci help-request page referenced by the skill](https://www.ablesci.com/assist/create)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown tables, JSON snippets, shell commands, browser actions, downloaded files, and progress-file updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a configured progress file, trigger browser downloads into a configured folder, create recurring monitoring tasks, and send notifications when configured.]

## Skill Version(s):

1.0.3 (source: release evidence, skill.json, CHANGELOG released 2026-04-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
