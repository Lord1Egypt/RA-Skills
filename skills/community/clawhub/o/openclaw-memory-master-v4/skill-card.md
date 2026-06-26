## Description: <br>
AI memory system for agents with iterative compression, lineage tracking, local memory files, and performance-oriented recall support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and run a local memory system that records decisions, organizes memory and knowledge indexes, and compresses accumulated context into lineage-aware summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Initialization rewrites agent-wide instruction and memory files. <br>
Mitigation: Back up and review AGENTS.md, MEMORY.md, and HEARTBEAT.md before installation or upgrade; treat the process as an agent-behavior migration. <br>
Risk: The installed behavior may include autonomous checks or actions beyond memory management. <br>
Mitigation: Remove or disable heartbeat instructions for email, calendar, social checks, commit or push actions, and automatic web learning unless those behaviors are explicitly desired. <br>
Risk: Local memory retention may capture sensitive conversation content. <br>
Mitigation: Clarify retention, deletion, logging, and local storage controls before using the skill with sensitive conversations. <br>
Risk: The database migration includes sample SQL INSERT rows. <br>
Mitigation: Remove sample INSERT rows before applying the migration to a real database. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/cp3d1455926-svg/openclaw-memory-master-v4) <br>
- [Project homepage](https://cp3d1455926-svg.github.io/openclaw-memory/) <br>
- [Iterative Compression Guide](docs/aaak-iterative-compression-guide.md) <br>
- [Performance Optimization Report](docs/performance-optimization-report.md) <br>
- [Test Results](TEST_RESULTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown memory files, JavaScript command output, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local workspace memory files and may migrate AGENTS.md, MEMORY.md, and HEARTBEAT.md during initialization.] <br>

## Skill Version(s): <br>
4.2.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
