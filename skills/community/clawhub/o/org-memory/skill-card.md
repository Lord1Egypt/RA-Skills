## Description: <br>
Extends the org-cli skill so the agent also persists its own memory (knowledge, observations, daily notes) to an org workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dcprevere](https://clawhub.ai/user/dcprevere) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to give an OpenClaw agent a dedicated org workspace for long-term memory, daily notes, TODOs, and graph-structured knowledge. It is intended for agents that already use org-cli and need persistent, searchable context across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist and reload user-related notes across sessions. <br>
Mitigation: Install it only when long-term org-based agent memory is desired, avoid saving secrets or sensitive personal data, and periodically review and prune the memory directory. <br>
Risk: Some write tools have weak file scoping and may write outside the configured memory workspace. <br>
Mitigation: Prefer an updated version that validates file paths before write tools run, and configure ORG_MEMORY_DIR, ORG_MEMORY_ROAM_DIR, and ORG_MEMORY_DB to trusted locations. <br>
Risk: The skill depends on an external org CLI binary. <br>
Mitigation: Use a trusted org CLI binary and set ORG_CLI_BIN explicitly when the default PATH resolution is not appropriate. <br>


## Reference(s): <br>
- [Memory architecture](references/memory-architecture.md) <br>
- [org-cli homepage](https://github.com/dcprevere/org-cli) <br>
- [org-cli releases](https://github.com/dcprevere/org-cli/releases) <br>
- [ClawHub skill page](https://clawhub.ai/dcprevere/org-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, text tool results, JSON-formatted org CLI output, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the org binary and configured ORG_MEMORY_* paths; session-start context may include memory.org and recent daily notes truncated to 32768 bytes per file.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter, plugin manifest, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
