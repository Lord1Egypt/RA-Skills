import os
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage

# ignore env load

# =========================
# Create State Schema
# =========================
class ChatState(TypedDict):
    query: str
    answer: str


# =========================
# Create Nodes
# =========================
def chat_node(state: ChatState) -> ChatState:
    """Single node: call chat model and store query & answer in state."""
    query = state.get("query", "").strip()

    llm = ChatOpenAI() # ignore params

    messages = [
        SystemMessage("You are a helpful assistant."),
        HumanMessage(query),
    ]

    result = llm.invoke(messages)
    return {"query": query, "answer": result.content}


# =========================
# Build Workflow
# =========================
def build_graph() -> StateGraph:
    graph = StateGraph(ChatState)
    
    graph.add_node("one chat node", chat_node)
    
    graph.add_edge(START, "one chat node")
    graph.add_edge("one chat node", END)
    return graph


if __name__ == "__main__":
    workflow = build_graph().compile()

    initial_state: ChatState = {
        "query": "My name is K. Tell me a joke.",
        "answer": "",
    }

    print("===Running invoke()===\nfinal state:")
    final_state = workflow.invoke(initial_state)
    print(final_state)
    
    print("===Testing memory===\nfinal state:")
    final_state = workflow.invoke({
        "query": "What is my name?"
    })
    print(final_state)

    print("\n===Running stream()===\nnode execution:")
    for step in workflow.stream(initial_state):
        for node_name, updated_state in step.items():
            print(f"{node_name} finished. Updated state: {updated_state}")
