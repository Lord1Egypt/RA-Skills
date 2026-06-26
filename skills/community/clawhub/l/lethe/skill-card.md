## Description: <br>
Use Lethe persistent memory for startup orientation, recall, logging, flags, and session compaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mentholmike](https://clawhub.ai/user/mentholmike) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Lethe Memory to orient an agent from local persistent memory, recall prior decisions and open work, record durable events, manage flags, and compact session history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory may store sensitive work context or personal data. <br>
Mitigation: Avoid logging secrets or personal data, and delete accidentally logged sensitive data through the API or UI. <br>
Risk: Using remote storage or exposing the local service can send memory data outside the intended host. <br>
Mitigation: Keep LETHE_API unset unless remote storage is intentional, keep the local service unexposed, and set LETHE_SESSION_ID explicitly on shared machines. <br>


## Reference(s): <br>
- [Lethe Memory on ClawHub](https://clawhub.ai/mentholmike/lethe) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Lethe API calls and the bundled lethe-log helper for memory operations.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
