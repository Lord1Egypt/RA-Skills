## Description: <br>
Track water and sleep with JSON file storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to have an agent record water intake and sleep or wake events to a local JSON file, then summarize recent water and sleep records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores water and sleep history in a local JSON file. <br>
Mitigation: Use it only if local storage of this history is acceptable, and review or delete {baseDir}/health-data.json when the records are no longer needed. <br>
Risk: Update and delete commands modify the stored log without a backup. <br>
Mitigation: Review the target record before running update or delete commands, and keep a separate backup when preserving history matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/litiao1224/healthcheck-litiao) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash and Node.js command snippets plus JSON file records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and updates {baseDir}/health-data.json locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
