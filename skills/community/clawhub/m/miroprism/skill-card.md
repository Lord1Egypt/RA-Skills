## Description: <br>
MiroPRISM is an adversarial two-round review protocol that requires reviewers to challenge Round 1 findings with independent evidence before synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeremyknows](https://clawhub.ai/user/jeremyknows) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use MiroPRISM to review architecture decisions, security-sensitive changes, open source releases, and other high-stakes artifacts where consensus drift is a risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review material may include proprietary code, secrets, regulated data, or private security findings, and review material may be shown to multiple subagents or stored locally under analysis/miroprism. <br>
Mitigation: Redact sensitive values before running the skill and keep analysis/miroprism out of public commits, backups, and shared artifacts when needed. <br>
Risk: Large artifacts increase exposure and cost because Round 2 sends the original artifact to each reviewer. <br>
Mitigation: Use Budget mode, external file references, or symmetric truncation for large artifacts while ensuring all reviewers receive the same input. <br>


## Reference(s): <br>
- [Miroprism on ClawHub](https://clawhub.ai/jeremyknows/miroprism) <br>
- [PRISM](https://github.com/jeremyknows/PRISM) <br>
- [Post-Launch Metrics Reference](references/post-launch-metrics.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance, Analysis] <br>
**Output Format:** [Markdown synthesis with review findings, verdicts, digest logs, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes review state and final synthesis under analysis/miroprism; can run standard, budget, or extended review modes.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
