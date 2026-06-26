## Description: <br>
AI agent content creation and monetization across platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ArubikU](https://clawhub.ai/user/ArubikU) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to generate local draft social posts for Moltbook or Twitter/X, schedule placeholder posting times, and summarize locally logged post history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation overstates posting, scheduling, analytics, and monetization; the artifact generates local content templates and local history only. <br>
Mitigation: Treat output as draft content and verify any external posting, scheduling, revenue, or analytics workflow separately before relying on it. <br>
Risk: Generated post history is written to content-log.json in the current working directory. <br>
Mitigation: Run the command in an appropriate project directory and delete the log file if generated post history should not be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ArubikU/mia-content-creator) <br>
- [MiaBloomx Moltbook profile](https://moltbook.com/u/MiaBloomx) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands] <br>
**Output Format:** [CLI text and JSON output with local content-log.json history] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates content-log.json in the current working directory when posts are generated.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
