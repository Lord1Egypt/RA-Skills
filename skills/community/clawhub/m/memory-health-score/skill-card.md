## Description: <br>
Provides a 0-100 health score for an agent memory system across completeness, freshness, structure, density, and consistency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidadong2359](https://clawhub.ai/user/weidadong2359) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to evaluate workspace memory files, spot stale or inconsistent memory state, and generate improvement recommendations before relying on agent memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Low health scores may lead to memory compression, index rebuilds, or issue cleanup that changes workspace state. <br>
Mitigation: Use report-only scoring by default and require explicit approval before compression, index rebuild, or issue cleanup. <br>
Risk: The health check reads local memory and issue files and writes a score report into the workspace. <br>
Mitigation: Run it only in the intended workspace and review the generated memory/health-score.json before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weidadong2359/memory-health-score) <br>
- [Agent amnesia prevention guide](artifact/agent-amnesia-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown instructions and JSON score reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled health check writes memory/health-score.json when run in a workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
