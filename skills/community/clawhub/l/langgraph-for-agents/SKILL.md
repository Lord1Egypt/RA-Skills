---
name: langgraph-for-agents
description: Use LangGraph/LangChain to build agents
---

# LangGraph for Agents

## When to use
- Use this skill when the user asks to build agents or multi-agent systems using LangGraph/LangChain.

## How to refer
### Integrated Reference Examples
Read the examples in `./references/` to understand common patterns. 
Start with `./references/README.md` for an overview, then read the target file, it will show more details.

### External Resources
[Search]
If the "search" tool is available, you can refine the query keywords and execute the search.

[Browse]
If the "browse" tool is available, you can visit the following three websites:
- LangGraph Official GitHub Repository (https://github.com/langchain-ai/langgraph)
- LangGraph Official Documentation (https://docs.langchain.com/oss/python/langgraph/overview)
- LangChain Official Documentation (https://docs.langchain.com/oss/python/langchain/overview)

[Fetch]
If the "fetch" tool is available, you can retrieve content from the following URL:
- Context-7 LangGraph (https://context7.com/websites/langchain_oss_python_langgraph/llms.txt?topic={}&tokens={})

The `topic` and `tokens` query parameters can be adjusted based on your needs:
- `topic`: Filter the documentation to a specific subject area (e.g., `interrupt`, `streaming`, `checkpoints`, `tools`).
- `tokens`: Control the response length (e.g., `10000` for detailed docs, `5000` for concise output).
- Example: To fetch ~10k tokens of LangGraph docs focused on the interrupt feature:
  `https://context7.com/websites/langchain_oss_python_langgraph/llms.txt?topic=interrupt&tokens=10000`


## Project Structure
For demos or tests, use a single .py file. For production-grade applications, use:
```
├── app/                      
│   ├── api/        # API endpoints
│   ├── backend/    # LangGraph/LangChain logic
│   └── frontend/   # User interface
├── .env.example
├── requirements.txt
└── README.md
```

## Process for Agent System Design
### Step 1: Determine System Level
- Single-Agent System: Focus on the internal structure of one agent.
- Multi-Agent System: Focus on collaboration and communication between multiple agents.

### Step 2: Choose Framework
- LangGraph: Best for stateful, complex workflows.
- LangChain: Best for standard agent patterns based on tool calling.

### Step 3: Design Specific Implementation
#### For Single-Agent Systems:
- With LangGraph: Build a workflow with several nodes, or implement a ReAct Agent with manual tool_node.
- With LangChain: Build a ReAct Agent by `create_agent` API.

#### For Multi-Agent Systems:
- With LangGraph:
  - Option 1: Treat each node as an independent agent, connecting them via the Graph API.
  - Option 2: Encapsulate a multi-node workflow as a single agent, calling other agents as tools.

- With LangChain:
  - Create a main ReAct Agent and encapsulate other agents as tools for collaboration.

## Build Philosophy
- Prefer Native: Check if a tool or integration already exists in LangChain before custom building.
- Single File First: Keep core logic in one file initially to simplify debugging.
- Clean Code: Provide only essential comments and use clear, descriptive variable names.
- Real Data: Use actual API URLs and schemas whenever possible.
