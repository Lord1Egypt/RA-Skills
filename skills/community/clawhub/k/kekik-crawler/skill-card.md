## Description:

Scrapling-only, deterministic web crawler with clean SRP architecture, presets, checkpointing, and JSONL/report outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keyiflerolsun](https://clawhub.ai/user/keyiflerolsun)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to run deterministic Scrapling-based crawls from seed URLs or search queries, producing JSONL crawl data and summary reports for research and monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler can follow untrusted links to arbitrary network locations.

Mitigation: Run it only in an isolated environment with restricted network access, especially blocking localhost, private networks, and cloud metadata endpoints.

Risk: Research presets disable robots.txt checks by default.

Mitigation: Review or change preset settings before use so crawling respects robots.txt where required.

Risk: Crawled content is stored locally in output files and the SQLite cache.

Mitigation: Treat JSONL outputs, reports, checkpoints, and cache files as potentially sensitive and apply retention and access controls.

Risk: Dependencies are range-based rather than pinned.

Mitigation: Pin and review dependencies before operational deployment.

## Reference(s):

- [Kekik Crawler on ClawHub](https://clawhub.ai/keyiflerolsun/skills/kekik-crawler)
- [Publisher profile](https://clawhub.ai/user/keyiflerolsun)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, JSON, Markdown guidance]

**Output Format:** [Markdown guidance with CLI commands; runtime outputs are JSONL crawl files, JSON reports, checkpoints, and a SQLite cache.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses seed URLs or search queries, optional presets, crawl limits, concurrency, robots.txt controls, SSL verification controls, and output path settings.]

## Skill Version(s):

0.1.0-rc1 (source: release metadata, pyproject.toml, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
