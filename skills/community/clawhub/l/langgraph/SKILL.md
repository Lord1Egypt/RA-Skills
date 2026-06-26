### Skill Name: LangGraph Agent Pipeline Architect

### Skill Description

This skill instructs an Agent to architect, build, and deploy robust AI agent pipelines using LangGraph. It focuses on moving beyond simple linear chains to create stateful, cyclical, and multi-actor systems. The Agent will learn to define state schemas, construct graph nodes, manage control flow with conditional edges, and implement production-grade features like human-in-the-loop and persistence.

### Core Instruction Set

#### 1. State Schema Definition

The foundation of any LangGraph pipeline is the `State`. The Agent must define a shared state object that acts as the "memory" passed between nodes.

- **TypedDict:** Use Python's `TypedDict` to define the structure of the state.
- **Reducers:** Crucially, define how state updates are handled. Use `Annotated` types with reducers (e.g., `add_messages`) to specify that certain fields (like chat history) should be appended to rather than overwritten.
- **Example:**

```
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    # 'add_messages' ensures new messages are appended to the history
    messages: Annotated[list[BaseMessage], add_messages]
    query_type: str  # A simple string field for routing logic
```

#### 2. Graph Construction & Nodes

Treat the agent pipeline as a directed graph where nodes represent units of computation.

- **StateGraph Initialization:** Initialize the graph builder using `StateGraph(AgentState)`.
- **Node Definition:** Define nodes as standard Python functions (or LangChain runnables) that accept the current `state` and return a dictionary of updates.
    - **Logic:** Nodes can perform LLM calls, execute tools, or process data.
    - **ToolNode:** For standard tool execution, utilize the prebuilt `ToolNode` to handle tool calling logic automatically.
- **Adding Nodes:** Register functions to the graph using `graph.add_node("node_name", function)`.

#### 3. Control Flow & Edges

Define the logic that dictates how the agent moves from one step to the next.

- **Entry Point:** Set the starting node using `graph.set_entry_point("node_name")` or `graph.add_edge(START, "node_name")`.
- **Normal Edges:** Use `graph.add_edge("node_a", "node_b")` for deterministic transitions (e.g., Step 1 always goes to Step 2).
- **Conditional Edges (Routing):** Use `graph.add_conditional_edges()` to implement dynamic logic.
    - **Router Function:** Create a function that inspects the `state` and returns a string indicating the next node (e.g., checking if the LLM invoked a tool).
    - **Mapping:** Map the router's return values to specific node names or `END`.
    - **Cycles:** To create an agent loop, map the tool execution node back to the agent node (e.g., `tools` → `agent`).

#### 4. Advanced Production Patterns

To build production-ready pipelines, the Agent must implement specific architectural patterns.

- **Human-in-the-Loop:**
    - Use `interrupt_before=["node_name"]` in the `compile` method. This pauses the graph execution before a specific node (e.g., before executing a sensitive tool), allowing a human to approve or modify the state before resuming.
- **Persistence (Checkpoints):**
    - Configure a `checkpointer` (e.g., `MemorySaver` or a database) when compiling the graph. This allows the agent to pause, resume, and retain memory across long-running conversations or distinct threads.
- **Streaming:**
    - Implement streaming to provide real-time feedback. Use `app.stream(inputs)` to yield events as they happen, rather than waiting for the final response.

#### 5. Execution & Compilation

Finalize the pipeline by compiling the graph into a runnable application.

- **Compilation:** Call `graph.compile()` to validate the graph structure and prepare it for execution.
- **Invocation:** Run the agent using `app.invoke(inputs)` for standard execution or `app.stream(inputs)` for streaming responses.

### Troubleshooting & Common Pitfalls

#### Infinite Loops

- **Symptom:** The agent cycles between nodes (e.g., Agent → Tool → Agent) forever.
- **Fix:** Ensure your router logic has a clear exit condition (returning `END`). Verify that the LLM is correctly bound to tools so it knows when to stop calling them.

#### State Overwriting

- **Symptom:** Chat history disappears after a node update.
- **Fix:** Check your `State` definition. Ensure you are using `Annotated[..., add_messages]` for the messages list. Without the reducer, the default behavior is to overwrite the key with the new value.

#### "Graph structure is not valid"

- **Symptom:** Compilation fails.
- **Fix:** Ensure every node referenced in an edge is actually added to the graph via `add_node`. Also, ensure there are no "orphan" nodes that are unreachable from the entry point.

### Skill Extension Suggestions

#### Multi-Agent Collaboration

Expand the pipeline to include multiple specialized agents (e.g., "Researcher", "Writer", "Editor"). Use a "Supervisor" node to route tasks between them based on the current context.

#### Subgraphs

Teach the Agent to encapsulate complex logic into a subgraph (a graph within a graph). This allows for modular design, where a "Research" node might actually trigger an entire internal research workflow.

#### Dynamic Tool Binding

Implement logic where the available tools change dynamically based on the user's query or the current state, requiring the Agent to re-bind the LLM to different tool sets at runtime.

