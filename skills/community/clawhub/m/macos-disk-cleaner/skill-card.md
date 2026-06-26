## Description: <br>
Analyze and reclaim macOS disk space through intelligent cleanup recommendations. This skill should be used when users report disk space issues, need to clean up their Mac, or want to understand what's consuming storage. Focus on safe, interactive analysis with user confirmation before any deletions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wusuiling-if](https://clawhub.ai/user/wusuiling-if) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to investigate macOS disk usage, identify cleanup candidates, and receive conservative, confirmation-based cleanup commands and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup commands or helper scripts can permanently delete broad local paths. <br>
Mitigation: Review every target before execution, prefer analysis-only use, use Trash or backups for recoverability, and avoid running deletion helpers on home, system, project-root, credential, or important-data directories. <br>
Risk: Commands involving sudo or broad rm -rf patterns can remove system-wide or user data beyond the intended cleanup target. <br>
Mitigation: Avoid sudo unless the user explicitly accepts the administrator-level impact, narrow commands to specific confirmed paths, and require a dry-run or manual review before cleanup. <br>
Risk: Docker and development-environment cleanup can remove databases, volumes, caches, or build artifacts that may be expensive or impossible to recreate. <br>
Mitigation: List exact objects, inspect database-like volumes, avoid broad prune commands, and delete only specifically confirmed objects. <br>


## Reference(s): <br>
- [macOS Cleanup Targets Reference](references/cleanup_targets.md) <br>
- [Mole Integration Guide](references/mole_integration.md) <br>
- [Safety Rules for macOS Cleanup](references/safety_rules.md) <br>
- [Mole](https://github.com/tw93/Mole) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and cleanup reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user review before deletion; may include analysis-only recommendations, dry-run previews, and manually executed cleanup commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
