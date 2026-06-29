## Description: <br>
HipoolMemorySystem provides a lightweight pure-C memory engine for AI agents, with key-value storage, tag and time-range search, named shards, WAL recovery, and snapshot support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hualang-c](https://clawhub.ai/user/hualang-c) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add a local embedded memory layer for storing, retrieving, searching, and snapshotting agent memory in constrained environments. It is best suited for local memory workflows where a small C binary and explicit persistence behavior are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists agent memory data in plaintext local storage. <br>
Mitigation: Avoid storing secrets or personal data; protect the storage directory, backups, and retention policy before use. <br>
Risk: Benchmark and test scripts can delete temporary benchmark paths and may start a Redis daemon. <br>
Mitigation: Review scripts before running them and execute benchmarks only in an isolated disposable environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hualang-c/hipool) <br>
- [README](artifact/README.md) <br>
- [English Skill Documentation](artifact/hipool-skill-en.md) <br>
- [Benchmark Results](artifact/benchmark_results.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with C source files and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local build and usage guidance for a C memory engine; runtime data is persisted in local memory_data paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
