## Description: <br>
Unified health monitoring dashboard that consolidates skill quality, dependency security, cleanup needs, and protected skills status into a single health check report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace maintainers use this skill to generate a concise health report for an OpenClaw workspace, including skill structure, dependency status, cleanup recommendations, and protected skill presence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dependency status is a lightweight package manifest check and may not identify actual vulnerabilities. <br>
Mitigation: Run a dedicated lockfile-aware vulnerability scanner, such as npm audit or another approved security tool, before making security decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-workspace-health-dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [JavaScript objects and human-readable text dashboard] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes an overall score, per-check status, cleanup counts, dependency count, and quick boolean health result.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
