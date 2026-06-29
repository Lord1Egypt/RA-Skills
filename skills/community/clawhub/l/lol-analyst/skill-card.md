## Description: <br>
lol-analyst queries League of Legends summoner profiles, ranked stats, match history, champion mastery, and improvement-oriented analysis using the Riot Games API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players, coaches, and agent users can query League of Legends account, ranked, match-history, and champion-mastery data, then receive generated reports and Chinese-language interpretation to guide gameplay improvement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Riot Games API key and can store it in plaintext at ~/.lol-analyst/config.json when setup mode is used. <br>
Mitigation: Prefer RIOT_API_KEY in the environment for routine use; if setup mode is used, restrict access to the machine and rotate or remove the key after use. <br>


## Reference(s): <br>
- [Riot Developer Portal](https://developer.riotgames.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, html, json, shell commands, configuration] <br>
**Output Format:** [CLI text plus local HTML or JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RIOT_API_KEY or an API key provided through setup or CLI arguments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
