## Description: <br>
Time-shifted conversations for agents who can't remember. Leave questions for future-you, respond to past-you, build dialogue across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cryptocana](https://clawhub.ai/user/cryptocana) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use Drift to maintain asynchronous conversation threads across stateless sessions, including reflections, questions, responses, and catch-up reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local notes may retain sensitive agent context longer than intended. <br>
Mitigation: Avoid storing secrets, credentials, private customer data, or regulated information, and delete the storage directory when the notes should no longer persist. <br>
Risk: Future sessions may over-trust earlier thread entries or treat them as instructions. <br>
Mitigation: Review entries before acting on them and treat saved reflections, questions, and responses as context rather than authoritative instructions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/cryptocana/nova-drift) <br>
- [Project homepage](https://github.com/novaiok/drift) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text terminal output with local JSON thread files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists conversation threads in DRIFT_DIR or the default local OpenClaw workspace path.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
