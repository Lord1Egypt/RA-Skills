## Description: <br>
Fetches the latest 50 posts from a specified Jike Topic, filters posts from the last 24 hours, analyzes valuable posts, and writes a daily digest Markdown document in Simplified Chinese. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redisread](https://clawhub.ai/user/redisread) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to help readers and operators of Jike Topics produce a concise daily digest of recent, valuable posts. The workflow is intended for users who can provide a Topic ID and want a Markdown summary with analysis, practical suggestions, and inspiration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rerunning the skill for the same topic and date may clear or replace existing related digest files in the chosen output folder. <br>
Mitigation: Set the base directory deliberately, preferably to a dedicated digest folder, and review the target path before rerunning. <br>
Risk: The workflow depends on a local autocli setup to fetch Jike content. <br>
Mitigation: Install and use the skill only where that local autocli access is intended, configured, and authorized for the requested Topic ID. <br>


## Reference(s): <br>
- [Output template](references/output-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/redisread/jike-digest) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown daily digest with YAML frontmatter, per-post analysis, a topic summary, Top 3 selections, and reader suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a required Jike Topic ID, an optional base directory, and a default 24-hour filtering window.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
