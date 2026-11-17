## Description:

Fetch and filter news from multiple sources with stopwords and blacklist support for IT, cybersecurity, and general news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huberteff](https://clawhub.ai/user/huberteff)

### License/Terms of Use:


## Use Case:

Agents can use this skill to retrieve grouped headline lists for general, IT, and cybersecurity news while filtering unwanted topics with a blacklist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to multiple news sites and RSS feeds.

Mitigation: Install only where outbound network access to the listed news sources is acceptable and restrict egress when handling sensitive environments.

Risk: The browser-based fetcher launches Chromium with sandboxing disabled and uses Puppeteer dependencies flagged by the security summary.

Mitigation: Prefer the RSS-based Python script, or require Chromium sandboxing, updated dependencies, and review before trusting the browser fetcher.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huberteff/skills/hfnews)
- [Tagesschau](https://www.tagesschau.de/)
- [FAZ](https://www.faz.net/aktuell/)
- [WiWo](https://www.wiwo.de/)
- [Sueddeutsche](https://www.sueddeutsche.de/)
- [Spiegel](https://www.spiegel.de/)
- [Mittelbayerische](https://www.mittelbayerische.de/lokales/stadt-regensburg)
- [Heise](https://www.heise.de/)
- [Golem](https://www.golem.de/)
- [Slashdot](https://slashdot.org/)
- [The Hacker News](https://thehackernews.com/)
- [BleepingComputer](https://www.bleepingcomputer.com/)
- [Logbuch Netzpolitik](https://logbuch-netzpolitik.de/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text grouped by news category with headline titles and URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports all categories by default or a single requested category.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
