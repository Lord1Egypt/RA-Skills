## Description: <br>
Enforces repository-defined contribution policy before any GitHub interaction (issues, PRs, comments, reviews). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therealhesreallyhim](https://clawhub.ai/user/therealhesreallyhim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when contributing to repositories they do not own, including opening issues, pull requests, comments, reviews, or discussion responses. It helps ensure repository policies, templates, duplicate-search expectations, pacing norms, and maintainer requests are followed before outward GitHub interaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outward GitHub actions can violate repository rules or create duplicate/disruptive interactions if policies and existing work are not checked first. <br>
Mitigation: Read repository contribution documents and templates, search for related issues and pull requests, slow repeated interactions, and stop when policy requirements cannot be satisfied. <br>
Risk: The skill may refuse to proceed when repository policies are missing, ambiguous, security-sensitive, or impossible to satisfy. <br>
Mitigation: Treat refusal as a governance safeguard and ask the user for missing context, permissions, or maintainer guidance before taking outward action. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Markdown guidance with repository-policy checks and stop conditions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no code execution, API credentials, or external tool integration are defined by the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
