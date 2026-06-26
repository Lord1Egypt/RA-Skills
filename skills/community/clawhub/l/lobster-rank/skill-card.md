## Description: <br>
Scans locally installed OpenClaw skills, collects structural metadata and heuristic signals, submits them to the Lobster ranking server for scoring, and lets the user confirm uploading the result to a public leaderboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bifang988](https://clawhub.ai/user/bifang988) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to scan their installed skill set, receive a server-side Lobster capability score, and optionally publish the confirmed result to the leaderboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends installed OpenClaw skill metadata, heuristic flags, and a Lobster API key to the publisher-operated ranking service. <br>
Mitigation: Run with --dry-run first, review the collected metadata, and use a dedicated Lobster API key when submitting. <br>
Risk: A confirmed score can be uploaded to a public leaderboard. <br>
Mitigation: Confirm upload only when the user intends to publish the score; otherwise stop after reviewing the pending result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bifang988/lobster-rank) <br>
- [Lobster Rank leaderboard](https://lobster-rank.wondercv.com) <br>
- [Lobster Rank account and API key page](https://lobster-rank.wondercv.com/me) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text score summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run inspection, score submission, and explicit confirmation before public leaderboard upload.] <br>

## Skill Version(s): <br>
3.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
