## Description: <br>
Detects time and space complexity hotspots via AST scan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers use this skill before performance-sensitive merges to scan target source files for likely time and space complexity hotspots, rank findings by severity, and produce an actionable performance review report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may inspect code or run performance-review tooling against a selected deployment or workspace. <br>
Mitigation: Use explicit prompts that scope the target files or deployment, and review the generated findings before allowing edits. <br>
Risk: Static complexity findings may be false positives or may not reflect runtime impact. <br>
Mitigation: Confirm important findings with profiling, benchmarks, before-and-after measurements, or manual hotspot sampling before accepting fixes. <br>
Risk: Suggested schema, migration, digest-table, fetch-strategy, or optimization changes could alter application behavior. <br>
Mitigation: Treat proposed changes as review candidates and require human approval plus tests or benchmark evidence before merging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-pensive-performance-review) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/athola) <br>
- [Clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown report with severity-grouped findings, source locations, suggestions, tier coverage, and optional command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are informational and should be confirmed with profiling, benchmarks, or manual review before fixes are accepted.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
