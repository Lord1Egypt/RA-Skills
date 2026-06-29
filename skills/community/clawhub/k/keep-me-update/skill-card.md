## Description: <br>
Generates daily tech, AI, and developer news digests from RSS feeds and web search after an interactive setup flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nemocccc](https://clawhub.ai/user/nemocccc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill in Hermes, OpenClaw, or compatible SKILL.md agents to create current tech, AI, and developer news digests with source links. It can print the digest to the terminal or write it as a local Markdown file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public RSS, news, and web search pages during normal use. <br>
Mitigation: Use it only where outbound public web access is acceptable, and review source links before relying on the digest. <br>
Risk: The skill saves local preferences and caches, and may write digest files under a chosen folder. <br>
Mitigation: Use a dedicated output directory and do not put API keys or other secrets in the skill YAML configuration. <br>
Risk: News links and feed entries can become stale, blocked, or unavailable. <br>
Mitigation: Keep the built-in link verification flow enabled and rerun later if the available source pool is too small. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nemocccc/keep-me-update) <br>
- [Project homepage](https://github.com/Nemocccc/KeepMeUpdate) <br>
- [Configuration flow reference](references/config-flow.md) <br>
- [RSS feed behavior reference](references/feed-behavior.md) <br>
- [Hermes Agent documentation](https://hermes-agent.nousresearch.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Terminal text or Markdown digest files with source links; configuration is stored as local YAML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create user_config.yaml, RSS cache and seen files, and dated digest files when file output is selected.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
