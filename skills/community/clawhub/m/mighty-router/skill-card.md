## Description: <br>
Enforces risk-based coding profiles, impact mapping, adversarial planning, and strict verification gates before making edits, audits, or structural modifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnnymaconny](https://clawhub.ai/user/johnnymaconny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use Mighty Router to classify coding, audit, and verification requests into risk-based execution profiles, escalating high-risk edits to stricter planning and verification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make agent responses more rigid and concise than a general coding assistant. <br>
Mitigation: Use it when stricter planning, verification, and high-risk edit handling are desired; disable it when flexible response style is more important. <br>
Risk: High-risk path rules can escalate routine work into a forensic workflow based on default paths or project configuration. <br>
Mitigation: Review .mightyrc or .mighty.json high_risk_paths before use and confirm that the selected profile fits the task. <br>
Risk: Forensic workflows may propose shell commands for verification. <br>
Mitigation: Review proposed commands and scope before execution, especially for tasks touching security-sensitive files or credentials. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown text with concise bullets, verification summaries, optional XML-tagged sections, and shell command plans.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Profile selection can change response structure, and high-risk routing may depend on .mightyrc or .mighty.json configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
