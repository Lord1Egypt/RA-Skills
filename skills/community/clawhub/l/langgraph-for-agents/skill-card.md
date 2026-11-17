## Description:

Use LangGraph/LangChain to build agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zachysun](https://clawhub.ai/user/zachysun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design and implement single-agent and multi-agent systems with LangGraph and LangChain patterns, including ReAct agents, workflows, routing, memory, streaming, RAG, and human-in-the-loop flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the included LLM, search, RAG, or memory examples can send prompts, documents, search queries, or memory contents to configured model, embedding, web, or Tavily providers.

Mitigation: Use non-sensitive test data by default, and add consent, redaction, provider controls, and per-user memory isolation before using private or user-specific data.

## Reference(s):

- [LangGraph Usage Library](references/README.md)
- [LangGraph Official GitHub Repository](https://github.com/langchain-ai/langgraph)
- [LangGraph Official Documentation](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangChain Official Documentation](https://docs.langchain.com/oss/python/langchain/overview)
- [Context-7 LangGraph Documentation](https://context7.com/websites/langchain_oss_python_langgraph/llms.txt?topic={}&tokens={})
- [LangGraph Human-in-the-Loop Example](references/langgraph_human_in_the_loop.py)
- [LangGraph Streaming Example](references/langgraph_streaming.py)
- [LangGraph Short-Term Memory Example](references/langgraph_workflow_st_mem.py)
- [LangGraph Long-Term Memory Example](references/langgraph_workflow_lt_mem.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include application structure recommendations and references to local example files.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
