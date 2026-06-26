## Description: <br>
A proactive memory distillation skill that maintains MEMORY.md through scheduled review, manual memory review triggers, and Obsidian indexing requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teman2050](https://clawhub.ai/user/teman2050) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users use Dream to keep active memory concise, archive older memory into a local ledger, and detect when forgotten memory reappears. It is intended for agents that need ongoing personal or project memory maintenance across conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently rewrite active memory during scheduled or triggered distillation. <br>
Mitigation: Review MEMORY.md and the monthly review logs regularly, and use narrower triggers or confirmations before enabling unattended operation. <br>
Risk: The skill keeps a permanent ledger archive even when active memory is cleared. <br>
Mitigation: Avoid storing sensitive topics unless permanent retention is acceptable, and add a real purge workflow before relying on forget behavior for deletion. <br>
Risk: The configured vault path controls where long-term memory artifacts are stored. <br>
Mitigation: Confirm DREAM_VAULT_PATH before initialization and restrict access to the workspace and vault directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teman2050/memory-file-manager-teman) <br>
- [Project homepage](https://github.com/teman2050/dream-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and local file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains MEMORY.md, ledger files, review logs, and Obsidian index files in the configured local workspace and vault.] <br>

## Skill Version(s): <br>
0.2.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
