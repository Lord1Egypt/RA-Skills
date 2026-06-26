## Description: <br>
LLM Memory Integration - interface layer with automation hooks that can pull a private enhancement package from a CNB repository after installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xkzs2007](https://clawhub.ai/user/xkzs2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local memory storage, SQLite FTS search, and memory CRUD interfaces to an OpenClaw workspace. When hooks are enabled, it also installs or checks a private enhancement package that may provide higher-performance memory features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install hook automatically downloads unpinned private code from a CNB repository. <br>
Mitigation: Install only after trusting the publisher and repository, or disable hooks and manually inspect and pin the private package before installation. <br>
Risk: The startup hook contacts Git to check the private package state. <br>
Mitigation: Review hook behavior before enabling startup execution and restrict network access if automatic Git checks are not acceptable. <br>
Risk: The package writes under the local memory directory and the skill's src/privileged path. <br>
Mitigation: Confirm the declared filesystem paths are acceptable for the workspace and monitor those directories after installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xkzs2007/llm-memory-v8-fix) <br>
- [CNB private enhancement package endpoint](https://cnb.cool/llm-memory-integrat/llm) <br>
- [Architecture Notes](docs/ARCHITECTURE.md) <br>
- [Hooks README](hooks/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and Python interfaces with optional shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local memory records, search results, hook status logs, and setup guidance.] <br>

## Skill Version(s): <br>
8.0.1 (source: server evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
