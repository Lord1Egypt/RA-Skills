## Description: <br>
Supadata helps agents search YouTube data, retrieve transcripts and metadata, map website links, and scrape web pages through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to perform read-oriented Supadata account, YouTube, transcript, link-mapping, and web-scraping tasks without directly handling Supadata API tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Supadata account and sends Supadata requests through OOMOL as an intermediary. <br>
Mitigation: Install only when comfortable with OOMOL-mediated access, and review the OOMOL account connection and credential scope before use. <br>
Risk: Connector actions run through shell commands and depend on the live connector schema for valid payloads. <br>
Mitigation: Inspect the target action schema before building a payload, and approve any future write or destructive connector action only after checking the exact target and effect. <br>


## Reference(s): <br>
- [ClawHub Supadata Skill](https://clawhub.ai/oomol/oo-supadata) <br>
- [Supadata Homepage](https://supadata.ai/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with oo CLI shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects with data and meta.executionId when actions run successfully.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
