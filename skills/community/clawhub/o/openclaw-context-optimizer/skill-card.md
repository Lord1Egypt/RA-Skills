## Description: <br>
Intelligently compresses and optimizes agent context to reduce token usage using deduplication, pruning, summarization, and adaptive learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to compress long or repetitive agent context, track token savings, and manage local optimization history. It is suited to workflows where automatic prompt rewriting can be reviewed and constrained. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic prompt rewriting can remove or alter context needed for high-stakes or instruction-sensitive tasks. <br>
Mitigation: Disable the skill or review compressed context before use for legal, medical, financial, security, or compliance-sensitive work. <br>
Risk: Local optimizer records can include wallet-linked usage and compression history. <br>
Mitigation: Review local storage contents and retention expectations before use, especially on shared machines. <br>
Risk: The payment workflow is under-scoped and not production-grade. <br>
Mitigation: Use strict spending caps, recipient allowlists, and human approval before connecting a funded wallet or allowing renewals. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AtlasPA/openclaw-context-optimizer) <br>
- [README](README.md) <br>
- [Agent Payments via x402](AGENT-PAYMENTS.md) <br>
- [ContextCompressor API Documentation](src/COMPRESSOR_API.md) <br>
- [Storage Implementation](STORAGE_IMPLEMENTATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, local code hooks, CLI output, and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces compressed context and local analytics; setup requires Node.js and writes local optimizer records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
