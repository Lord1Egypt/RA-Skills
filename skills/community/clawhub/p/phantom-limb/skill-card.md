## Description: <br>
Detects phantom dependencies: references to missing environment variables, stale configuration, deprecated APIs, outdated docs, and other code assumptions that no longer match reality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcools1977](https://clawhub.ai/user/jcools1977) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect repositories for stale references, mismatched assumptions, and phantom dependencies before onboarding, refactors, architecture reviews, or production deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository analysis may inspect .env, CI/CD, and deployment files that contain sensitive values. <br>
Mitigation: Ask the agent to report variable names, file paths, and missing relationships without printing secret values. <br>
Risk: Static analysis findings and remediation suggestions may be incomplete or misleading if schemas, deployment state, or API contracts are outdated. <br>
Mitigation: Review findings against current source files, deployment configuration, and API or database schemas before making changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jcools1977/phantom-limb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis report with prioritized findings and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports phantom type, severity, affected reference, observed reality, and suggested fix.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
