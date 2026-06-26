## Description: <br>
Monitor GitHub repositories for new releases and get alerts when tracked repos ship updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to track configured GitHub repositories and surface newly published releases for review or notification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release-check script can execute local Python code if a watched repository publishes a specially crafted release tag. <br>
Mitigation: Review or patch the shell script before installing, use safe JSON argument passing, track only trusted repositories, and run it with a least-privilege GitHub CLI account. <br>
Risk: Automatic scheduling can repeatedly execute the release-check workflow before the script is reviewed. <br>
Mitigation: Avoid cron or heartbeat automation until the script is fixed and the watched repository list is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rogue-agent1/github-release-watcher) <br>
- [Publisher profile](https://clawhub.ai/user/rogue-agent1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown/plain text release status with shell command usage and repository configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GitHub CLI authentication and stores last-seen release state in a local JSON file.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
