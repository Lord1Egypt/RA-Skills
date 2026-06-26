## Description: <br>
Enhanced memory retrieval support that combines an Ebbinghaus forgetting curve with a Hebbian co-occurrence graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents can use this skill to reason about local memory retrieval, reinforce associations between memories, and rank memories with use-count and time-decay signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory associations are stored on disk and may reveal sensitive context if secrets are included in memories. <br>
Mitigation: Avoid storing secrets in memories and review or delete ~/.config/cortexgraph/co_occurrence.db when needed. <br>
Risk: Some documented helper commands are not included in the artifact and could behave differently if supplied from another source. <br>
Mitigation: Inspect any missing helper scripts, keep a backup, and run only the included tracker or trusted scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guohongbin-git/memory-sync-enhanced) <br>
- [CortexGraph](https://github.com/prefrontal-systems/cortexgraph) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash, Python, JSON, and SQL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local SQLite co-occurrence database under ~/.config/cortexgraph when the tracker is run.] <br>

## Skill Version(s): <br>
2.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
