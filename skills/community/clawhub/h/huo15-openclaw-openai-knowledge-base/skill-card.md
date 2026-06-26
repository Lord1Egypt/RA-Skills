## Description: <br>
A knowledge-base skill that ingests URLs, files, text, WeChat articles, and GitHub sources, compiles raw material into structured Markdown wiki pages with LLM assistance, and supports search, graph generation, Obsidian sync, Bases views, and Daily Note workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to maintain an agent-scoped or shared Markdown knowledge base, compile source material into linked wiki entries, query those entries, and sync curated knowledge into Obsidian. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Knowledge-base content may be sent to an external LLM provider during compilation or question answering. <br>
Mitigation: Use agent scope for private material, review the configured provider before compiling, and avoid sending sensitive or untrusted documents unless the provider and data handling are acceptable. <br>
Risk: Bootstrap and all-agent installation helpers can make persistent workspace or agent-level changes. <br>
Mitigation: Run bootstrap-from-questionnaire.sh or install-all-agents.sh only after reviewing the scripts and confirming those broader changes are intended. <br>
Risk: Untrusted document compilation has a known filename path-containment concern in kb-llm.py. <br>
Mitigation: Do not compile untrusted documents until the path-containment issue is fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-openclaw-openai-knowledge-base) <br>
- [Publisher profile](https://clawhub.ai/user/zhaobod1) <br>
- [Karpathy LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) <br>
- [LLM Wiki v2 gist](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files, terminal text, shell commands, JSON configuration, and Mermaid graph text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create and update local raw, wiki, cache, log, index, Obsidian Bases, and Daily Note content.] <br>

## Skill Version(s): <br>
2.8.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
