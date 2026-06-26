## Description: <br>
Scrapling-only, deterministic web crawler with clean SRP architecture, presets, checkpointing, and JSONL/report outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keyiflerolsun](https://clawhub.ai/user/keyiflerolsun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and researchers use Kekik Crawler to run deterministic crawls from seed URLs or search queries, extract page data through plugins, and save JSONL crawl results with JSON reports. It supports normal, wide, deep, person-research, and deep-research crawl modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The crawler can access and store content from external sites, including search terms and page data in outputs, cache, reports, and checkpoints. <br>
Mitigation: Run it only against targets you are allowed to crawl and handle generated files as retained crawl data that may need review, access controls, or deletion. <br>
Risk: Research presets disable robots.txt checks, and the --no-robots option can bypass site crawl preferences. <br>
Mitigation: Use robots.txt checks for routine crawling and reserve robots-bypassing modes for authorized research contexts. <br>
Risk: Plugin loading depends on files from the configured plugin directory. <br>
Mitigation: Use only trusted plugin directories and review custom extractors before running the crawler. <br>
Risk: The --insecure option disables SSL verification. <br>
Mitigation: Avoid --insecure except in controlled test environments with known certificate issues. <br>
Risk: Dependencies are specified as lower bounds rather than exact pins. <br>
Mitigation: Install in a virtual environment and pin or audit dependencies before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keyiflerolsun/kekik-crawler) <br>
- [README](artifact/README.md) <br>
- [CHANGELOG](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, JSONL files, JSON reports] <br>
**Output Format:** [Command-line guidance and crawler outputs written as JSONL result files, JSON reports, SQLite cache, and checkpoint files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include crawled page content, extracted links, search terms, domain health summaries, cache entries, and checkpoint state.] <br>

## Skill Version(s): <br>
0.1.0-rc1 (source: server release metadata, pyproject.toml, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
