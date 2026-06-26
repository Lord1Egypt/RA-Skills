## Description: <br>
Gets upcoming and/or recent NBA game results for a specified team. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[highdeserthacker](https://clawhub.ai/user/highdeserthacker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve upcoming or recent NBA games for a selected team, including opponents, home/away status, tip-off times, and final scores when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup downloads an unpinned third-party Python script. <br>
Mitigation: Review the downloaded Python file, pin it to a specific commit, and add checksum or signature verification before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/highdeserthacker/nba-games) <br>
- [nba-schedule source repository](https://github.com/highdeserthacker/nba-schedule) <br>
- [nba-schedule.py helper script](https://raw.githubusercontent.com/highdeserthacker/nba-schedule/main/nba-schedule.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON array from the helper script, typically summarized as conversational text by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and an ESPN team ID; optional arguments control past and future day windows.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
