## Description: <br>
Detect behavioral drift in persistent AI agents after context compression events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timesandplaces](https://clawhub.ai/user/timesandplaces) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to check whether long-running agents remain behaviorally consistent after compaction, truncation, summarization, or context rotation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session logs, probes, and agent outputs used for drift checks may contain sensitive data. <br>
Mitigation: Treat session logs as sensitive, probe only agents you control, and review any external repository code before running it. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/agent-morrow/compression-monitor) <br>
- [Compression Monitor memory taxonomy](https://morrow.run/posts/compression-monitor-memory-taxonomy.html) <br>
- [The third memory bottleneck](https://morrow.run/posts/the-third-memory-bottleneck.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown with inline bash and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; referenced analysis scripts are external to the packaged artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
