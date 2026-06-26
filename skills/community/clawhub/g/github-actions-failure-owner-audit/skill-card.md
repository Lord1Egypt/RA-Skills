## Description: <br>
Audit failing GitHub Actions runs by actor ownership to expose who/workflow combinations generate the most CI noise and wasted minutes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and CI maintainers use this skill to analyze GitHub Actions run exports and identify which actors, owners, repositories, or workflows contribute the most failed runs and wasted CI minutes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub Actions exports and audit output can contain private repository names, branch names, actor identities, workflow details, or run URLs. <br>
Mitigation: Analyze only exports you are comfortable processing locally, scope RUN_GLOB and GitHub CLI exports narrowly, and avoid sharing raw output from private repositories. <br>
Risk: Using filters that are expected in version 1.2.0 against an older package can produce incomplete targeted triage. <br>
Mitigation: Verify the installed package version before relying on version-specific event, run-id, or run-url filters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-failure-owner-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Text or JSON audit reports, with shell-command examples and environment-variable configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local bash and python3. Reporting mode exits 0 by default; optional critical-threshold mode exits 1 when configured.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
