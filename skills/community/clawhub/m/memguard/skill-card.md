## Description: <br>
Memory leak and resource management scanner that detects unclosed handles, event listener leaks, circular references, unbounded caches, missing cleanup, dangling timers, and resource lifecycle issues across multiple languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use memguard to scan codebases for memory and resource lifecycle issues, install pre-commit checks, and generate resource health reports before changes reach production. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local scans read source files in the paths selected by the user. <br>
Mitigation: Run scans only on repositories and directories where local code inspection is acceptable. <br>
Risk: The hook install command can create or modify lefthook.yml and run checks on future commits. <br>
Mitigation: Use hook install only in repositories where pre-commit scanning is desired, review lefthook.yml afterward, and use hook uninstall if the hook is no longer needed. <br>
Risk: License keys may be stored in MEMGUARD_LICENSE_KEY or ~/.openclaw/openclaw.json. <br>
Mitigation: Keep the environment variable and OpenClaw configuration file under user control and out of commits or shared logs. <br>


## Reference(s): <br>
- [MemGuard website](https://memguard.pages.dev) <br>
- [ClawHub memguard release](https://clawhub.ai/suhteevah/memguard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output, Markdown reports, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scans local source files and may write lefthook.yml or .memguard-baseline.json when users invoke hook or baseline commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and script VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
