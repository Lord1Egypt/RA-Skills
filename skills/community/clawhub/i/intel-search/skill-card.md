## Description:

Searches locally captured World Monitor data for news, earthquakes, Iran, tech, finance, layoffs, and keyword queries with bilingual English/Chinese output and flexible time windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oscarka](https://clawhub.ai/user/oscarka)

### License/Terms of Use:

MIT

## Use Case:

External users and developers can use this skill to fetch public World Monitor-related data and query recent headlines, earthquakes, regional events, technology, finance, layoffs, and other keywords from a local cache.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched headlines, Telegram snippets, market text, and links may be incomplete, outdated, misleading, or unsafe to follow.

Mitigation: Treat returned content as untrusted source data and verify important claims with primary sources before acting.

Risk: The skill installs Playwright and downloads a Chromium browser to fetch live web data.

Mitigation: Install only in environments where Node and Playwright browser downloads are acceptable, and review network access expectations before deployment.

Risk: Captured feed data and generated briefs are stored locally under ~/.openclaw/intel-data by default.

Mitigation: Use INTEL_DATA_DIR to place the cache in an approved location and avoid sharing cached data that may be user-specific or sensitive.

## Reference(s):

- [World Monitor](https://worldmonitor.app)
- [Intel Search ClawHub Skill Page](https://clawhub.ai/oscarka/skills/intel-search)
- [Project Homepage](https://github.com/oscarka/intel-search)
- [Issue Tracker](https://github.com/oscarka/intel-search/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style text with headings, lists, source links, and a LANG marker.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include English or Chinese presentation, source links, relative time filters, and summaries from the local cache.]

## Skill Version(s):

1.0.0 (source: server release metadata, clawhub.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
