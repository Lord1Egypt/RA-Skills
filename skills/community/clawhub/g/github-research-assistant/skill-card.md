## Description: <br>
GitHub Research Assistant helps users analyze a GitHub repository across basic information, purpose, tech stack, usage, examples, and technical architecture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luochang212](https://clawhub.ai/user/luochang212) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to quickly understand a GitHub repository, including its purpose, technology choices, setup, examples, and architecture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository analysis may require broad inspection of files or command output from the target repository. <br>
Mitigation: Keep analysis scoped to repositories you intend to inspect, and review proposed shell commands or file mutations before allowing them. <br>
Risk: The generated repository report may contain incomplete or outdated conclusions if important files are missing or skipped. <br>
Mitigation: Review the report against the repository source and prioritize core documentation, dependency files, and main source modules. <br>


## Reference(s): <br>
- [Chinese reference guide](references/skill-cn.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, shell commands] <br>
**Output Format:** [Markdown report with repository facts, analysis, examples, and command suggestions when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prioritizes core files and directories for larger repositories.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
