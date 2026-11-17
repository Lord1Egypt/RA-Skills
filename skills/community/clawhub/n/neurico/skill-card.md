## Description:

Autonomous research framework that orchestrates AI agents (Claude Code, Codex, Gemini) to design, execute, analyze, and document scientific experiments from a structured YAML research idea.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laoliu5280](https://clawhub.ai/user/laoliu5280)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to run an autonomous research workflow that turns a YAML research idea into experiment code, results, plots, a LaTeX paper draft, and optional GitHub repository output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous research execution can generate and run code that may produce incorrect results or unsafe changes.

Mitigation: Review generated plans, code, and experiment outputs before relying on them or publishing results.

Risk: Installation instructions include unpinned Docker images and a curl-based native installer path.

Mitigation: Pin container image digests and inspect install scripts before execution.

Risk: GitHub publishing requires a token and may expose generated work if repository visibility is not controlled.

Mitigation: Use the narrowest GitHub token scope possible and run with --no-github or --private unless public publishing is intended.

Risk: Research workflows may handle sensitive datasets, API keys, or model credentials.

Mitigation: Audit upstream runtime behavior and avoid providing sensitive data or credentials until the workflow is approved for the target environment.

## Reference(s):

- [NeuriCo ClawHub Skill Page](https://clawhub.ai/laoliu5280/skills/neurico)
- [NeuriCo Repository](https://github.com/ChicagoHAI/neurico)
- [NeuriCo Issues](https://github.com/ChicagoHAI/neurico/issues)
- [Idea Schema](https://github.com/ChicagoHAI/neurico/blob/main/ideas/schema.yaml)
- [Dockerfile](https://github.com/ChicagoHAI/neurico/blob/main/docker/Dockerfile)
- [Security Filtering Code](https://github.com/ChicagoHAI/neurico/blob/main/src/core/security.py)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Codex Repository](https://github.com/openai/codex)
- [Gemini CLI Repository](https://github.com/google-gemini/gemini-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown]

**Output Format:** [Markdown with YAML examples, bash commands, and file tree output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of experiment files, result artifacts, LaTeX paper drafts, and GitHub repository content.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
