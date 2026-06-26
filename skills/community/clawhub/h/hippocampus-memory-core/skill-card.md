## Description: <br>
Hippocampus Memory Core provides deterministic external memory for OpenClaw and coding agents using S3-Hipokamp to store durable facts, retrieve prior decisions, snapshot memory, and restore agent state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cezexPL](https://clawhub.ai/user/cezexPL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill to give agents durable, scoped memory for decisions, architecture context, deployment or debugging findings, snapshots, and restore workflows across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable memory can retain secrets, raw transcripts, sensitive personal data, or context from the wrong project. <br>
Mitigation: Store only high-signal facts, avoid secrets and raw transcripts, and keep memory scoped by workspace and agent before restoring it into future sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cezexPL/hippocampus-memory-core) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Text and Markdown instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no executable code or hidden install behavior.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
