## Description:

Gets upcoming and/or recent NBA game results for a specified team. Use this skill when asked about scheduled, upcoming, or past games for any NBA team.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highdeserthacker](https://clawhub.ai/user/highdeserthacker)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer questions about upcoming or recently completed NBA games for a specified team. It can look up team IDs, fetch schedule windows, and present opponents, home or away status, tip-off times, scores, and win or loss results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs a Python script downloaded from the current GitHub main branch without integrity checks.

Mitigation: Install only from trusted sources; prefer pinning and verifying the downloaded script or bundling a reviewed copy before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/highdeserthacker/skills/nba-games)
- [nba-schedule source repository](https://github.com/highdeserthacker/nba-schedule)
- [nba-schedule.py download URL](https://raw.githubusercontent.com/highdeserthacker/nba-schedule/main/nba-schedule.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON array from the script, typically summarized as conversational text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a local downloaded nba-schedule.py script.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
