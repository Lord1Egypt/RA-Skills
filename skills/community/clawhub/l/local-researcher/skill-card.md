## Description:

Local Researcher guides agents through setting up and using local LLM research workflows with Ollama or LMStudio to generate cited Markdown research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonia-sz](https://clawhub.ai/user/antonia-sz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to configure local LLM-backed research workflows, run iterative web research, and produce structured Markdown reports with cited sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is network-enabled research software, so search topics and provider API use may leave the local machine.

Mitigation: Review provider configuration before use and avoid sensitive research topics until privacy wording and network behavior are verified.

Risk: Install instructions include a curl-to-shell installer and an unpinned repository clone workflow.

Mitigation: Independently verify upstream source, version, and installer contents before executing installation commands.

Risk: Privacy claims may understate network and code-execution risks.

Mitigation: Treat generated setup steps as proposals, review commands before running them, and scan the skill before deployment.

## Reference(s):

- [Local Researcher Skill Page](https://clawhub.ai/antonia-sz/skills/local-researcher)
- [LMStudio](https://lmstudio.ai/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Ollama Model Library](https://ollama.com/library)
- [LangChain Academy](https://academy.langchain.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and Python examples; generated research reports are Markdown with citations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include environment variables, provider choices, installation steps, local command sequences, and cited research metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
