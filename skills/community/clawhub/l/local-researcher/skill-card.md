## Description: <br>
Local Researcher helps agents run privacy-oriented iterative web research with Ollama or LMStudio local LLMs and produce cited Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonia-sz](https://clawhub.ai/user/antonia-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and research teams use this skill to configure local-model research workflows, run iterative web searches, and generate structured Markdown reports with cited sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries, URLs, and fetched pages can be disclosed to external search providers or target websites. <br>
Mitigation: Avoid confidential subjects and sensitive internal identifiers unless using a trusted offline or self-hosted search path. <br>
Risk: Installer commands that pipe remote shell scripts can execute unreviewed code. <br>
Mitigation: Prefer package-manager installs or verified installer steps, and review remote installation scripts before running them. <br>
Risk: Local LLM processing does not make the overall workflow fully local when web search is enabled. <br>
Mitigation: Document configured search providers and disable or self-host search for privacy-sensitive research. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/antonia-sz/local-researcher) <br>
- [LMStudio](https://lmstudio.ai/) <br>
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) <br>
- [Ollama Model Library](https://ollama.com/library) <br>
- [LangChain Academy](https://academy.langchain.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Research outputs may include cited sources, summaries, workflow metadata, and configuration examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
