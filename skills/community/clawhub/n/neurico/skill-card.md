## Description: <br>
Autonomous research framework that orchestrates AI agents (Claude Code, Codex, Gemini) to design, execute, analyze, and document scientific experiments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laoliu5280](https://clawhub.ai/user/laoliu5280) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and researchers use this skill to install, configure, and run NeuriCo for autonomous research workflows that turn structured YAML ideas into experiments, code, results, LaTeX papers, and GitHub repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide use of an external autonomous research framework that runs generated code and can publish results to GitHub with broad account permissions. <br>
Mitigation: Prefer Docker, inspect or pin the external repository and container image, and review generated code and outputs before relying on them. <br>
Risk: GitHub tokens and research inputs may expose account permissions, confidential ideas, datasets, or credentials if configured incautiously. <br>
Mitigation: Start with --no-github or --private, use a temporary least-privilege GitHub token where possible, and avoid confidential material unless the provider and repository settings are acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/laoliu5280/neurico) <br>
- [NeuriCo repository](https://github.com/ChicagoHAI/neurico) <br>
- [ChicagoHAI profile](https://github.com/ChicagoHAI) <br>
- [NeuriCo idea schema](https://github.com/ChicagoHAI/neurico/blob/main/ideas/schema.yaml) <br>
- [NeuriCo configuration docs](https://github.com/ChicagoHAI/neurico#configuration) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [Codex CLI repository](https://github.com/openai/codex) <br>
- [Gemini CLI repository](https://github.com/google-gemini/gemini-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline bash commands and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers setup, provider selection, YAML idea input, run options, and expected generated research artifacts.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
