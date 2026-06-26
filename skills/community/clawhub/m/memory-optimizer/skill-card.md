## Description: <br>
Memory Optimizer helps OpenClaw agents index, deduplicate, search, and watch local memory markdown files using SHA-256 content hashes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SiriuSM00N](https://clawhub.ai/user/SiriuSM00N) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to keep long-running agent memory directories smaller and faster to search by incrementally indexing changed markdown files, removing stale chunks, and optionally running a background watcher. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill copies local OpenClaw memory markdown into a persistent index, so sensitive content in the watched memory folder can be retained in the index file. <br>
Mitigation: Avoid placing secrets in the watched memory folder and review the generated memory index according to local data-handling requirements. <br>
Risk: The optional watcher runs continuously in the background and updates the local memory index as markdown files change. <br>
Mitigation: Run the watcher only when continuous indexing is needed and stop it when no longer required. <br>
Risk: The documentation describes a quarterly archive command, but the referenced archive script is not present in the provided artifact. <br>
Mitigation: Do not configure the documented archive cron job unless the missing archive script is obtained and reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/SiriuSM00N/memory-optimizer) <br>
- [Artifact README](artifact/docs/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration instructions, Markdown] <br>
**Output Format:** [Markdown guidance with Python and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local indexing and watcher workflows for OpenClaw memory markdown files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
