## Description:

lol-analyst helps agents query Riot Games League of Legends data for summoner profiles, ranked stats, match history, champion mastery, and improvement-oriented analysis using a Riot Games API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External players, coaches, and agents use this skill to retrieve League of Legends account and match data and generate Chinese-language performance reports or improvement guidance for a Riot ID.

### Deployment Geography for Use:

Global, limited by Riot Games API regional availability and Riot API coverage.

## Known Risks and Mitigations:

Risk: A Riot API key may be stored in plaintext in a local config file.

Mitigation: Prefer the RIOT_API_KEY environment variable, avoid putting keys in shell history or logs, and review local config file permissions before use.

Risk: The skill depends on a third-party Riot API client package.

Mitigation: Install dependencies in an isolated virtual environment and review dependency versions before deployment.

## Reference(s):

- [Riot Developer Portal](https://developer.riotgames.com/)
- [ClawHub skill release](https://clawhub.ai/bettermen/skills/lol-analyst)

## Skill Output:

**Output Type(s):** [text, HTML files, JSON data, shell commands, configuration, guidance]

**Output Format:** [Console text plus generated HTML or JSON reports; setup guidance may be Markdown with shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RIOT_API_KEY or a local config file and queries Riot Games API regions supported by the skill.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
