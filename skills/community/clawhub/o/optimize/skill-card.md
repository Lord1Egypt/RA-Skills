## Description: <br>
Optimizes OpenClaw performance with diagnostics, memory cleanup, skill-load analysis, history cleanup, monitoring, and configuration guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhmza](https://clawhub.ai/user/zhmza) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose and improve OpenClaw responsiveness, memory use, startup time, skill loading, and accumulated history size. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: History cleanup can delete files from the OpenClaw memory workspace. <br>
Mitigation: Back up ~/.openclaw/workspace/memory before using --full, --clean-history, optimize(), auto_optimize(), or HistoryOptimizer cleanup APIs. <br>
Risk: Host-level cleanup behavior can affect system cache or runtime state. <br>
Mitigation: Run without sudo/root and review diagnostic or report output before enabling actions that change cache, history, or performance settings. <br>
Risk: Automated optimization may apply cleanup actions without enough interactive confirmation. <br>
Mitigation: Prefer report, diagnose, monitor, or dry-run style paths first, then invoke cleanup only after confirming the affected files and retention window. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhmza/optimize) <br>
- [Publisher profile](https://clawhub.ai/user/zhmza) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python snippets, configuration examples, and plain-text diagnostic reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local reports and propose or perform cleanup actions when invoked through the bundled scripts.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
