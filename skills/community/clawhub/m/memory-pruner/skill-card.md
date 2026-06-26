## Description: <br>
Manages agent memory by auto-pruning old or low-relevance entries, compressing duplicates, and reporting storage costs with safe defaults. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiuge897](https://clawhub.ai/user/jiuge897) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Memory Pruner to inspect, prune, compress, and configure persistent memory so stale, duplicate, or low-value entries do not accumulate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify persistent agent memory, which may remove useful context or change future agent behavior. <br>
Mitigation: Start with dry-run, require explicit confirmation before pruning, keep backups, and limit access to the intended memory directory. <br>
Risk: The package references a memory-pruner shell entry that is not included in the artifact. <br>
Mitigation: Do not run real pruning unless the executable is supplied from a trusted source and reviewed before installation. <br>


## Reference(s): <br>
- [Memory Pruner ClawHub page](https://clawhub.ai/jiuge897/memory-pruner) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [config.json](artifact/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and CLI-style text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Memory-modifying actions should be previewed with dry-run, confirmed by the user, and backed up before pruning.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
