## Description: <br>
Search indexers and manage Prowlarr through API-backed commands for release search, indexer health, indexer management, app sync, and system checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmagar](https://clawhub.ai/user/jmagar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to search Prowlarr indexers, inspect indexer status and statistics, manage enabled indexers, and sync indexer changes to connected apps such as Sonarr or Radarr. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Prowlarr API key for the configured instance. <br>
Mitigation: Store the key in the documented local config file or environment variable, restrict file access, and rotate the key if it is exposed. <br>
Risk: Indexer management commands can enable, disable, delete, or sync indexer changes to connected applications. <br>
Mitigation: Confirm indexer IDs and require explicit approval before running delete, enable, disable, or sync commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jmagar/prowlarr) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Prowlarr URL and API key from a config file or environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
