## Description: <br>
Provides memory CRUD and search interfaces with a SQLite FTS fallback, plus install and startup hooks that fetch a private enhancement package from CNB. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xkzs2007](https://clawhub.ai/user/xkzs2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local memory storage, CRUD operations, and full-text search to an OpenClaw workspace. Optional enhanced search, embedding, and performance features are supplied by a private package fetched during installation when hooks are enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically downloads and checks extra private code during installation or startup. <br>
Mitigation: Install only when that remote access is acceptable, review the fetched package before relying on it, and disable hooks when automatic installation is not desired. <br>
Risk: The private package is not described as pinned by checksum or signature in the release evidence. <br>
Mitigation: Prefer a release that vendors or pins the private package, verifies signatures or checksums, and makes remote installation explicit before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xkzs2007/llm-memory-publish) <br>
- [Publisher Profile](https://clawhub.ai/user/xkzs2007) <br>
- [CNB Private Enhancement Package](https://cnb.cool/llm-memory-integrat/llm) <br>
- [Architecture](docs/ARCHITECTURE.md) <br>
- [Hooks](hooks/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python API references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory database files and install a private package under the skill directory when lifecycle hooks are enabled.] <br>

## Skill Version(s): <br>
8.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
