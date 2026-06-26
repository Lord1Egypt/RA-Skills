## Description: <br>
Aggregates and scores technology news from configured RSS feeds, GitHub endpoints, and web sources to produce daily digests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pyh-pan](https://clawhub.ai/user/pyh-pan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to collect technology headlines, rank them by configurable relevance signals, and generate concise daily news digests or item lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled trigger configuration enables an auto-start daily digest with Telegram notifications. <br>
Mitigation: Review trigger_config.json before installation and disable auto_start or notifications if daily digest delivery is not wanted. <br>
Risk: Python dependencies are specified with lower-bound version ranges rather than pinned audited versions. <br>
Mitigation: Pin and audit requests, feedparser, and beautifulsoup4 before managed or enterprise deployment. <br>
Risk: The 109+ source claim is not fully supported by the bundled default implementation. <br>
Mitigation: Treat the source-count claim as unverified until the maintainer expands the configured sources or documents the source inventory. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pyh-pan/multi-source-news-digest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, configuration] <br>
**Output Format:** [Markdown-style digest text or JSON status/data objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports digest, list, and refresh actions using configurable source lists and scoring thresholds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, package.json, config.json, skill.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
