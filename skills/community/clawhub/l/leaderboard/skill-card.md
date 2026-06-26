## Description: <br>
Record scores, rank players, and analyze game stats with terminal leaderboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to record game scores, rank competitors, inspect recent leaderboard activity, search entries, and export local score data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Leaderboard entries are saved locally and can later be searched or exported. <br>
Mitigation: Use the skill for non-sensitive game data and avoid entering passwords, API keys, private notes, or other sensitive personal data. <br>
Risk: Exported JSON, CSV, or TXT files may expose locally stored leaderboard entries if shared. <br>
Mitigation: Review exported files before sharing them and remove sensitive or unintended entries from the local data directory. <br>


## Reference(s): <br>
- [ClawHub Leaderboard skill page](https://clawhub.ai/xueyetianya/leaderboard) <br>
- [Publisher profile](https://clawhub.ai/user/xueyetianya) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Terminal text with optional JSON, CSV, or TXT export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local logs and exports under ~/.local/share/leaderboard/.] <br>

## Skill Version(s): <br>
2.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
